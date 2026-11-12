"""Local, resumable narration from the registered original human reference.

Never edits an existing waveform. A new seed or wording requires a new take.
"""
import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def words(text, language='en'):
    text = text.casefold().replace('’', "'")
    if language in ('zh', 'ja', 'yue'):
        return re.findall(r'[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff]|[a-zа-яё]+|\d+', text)
    return re.findall(r"[\w]+(?:['’][\w]+)?", text)


def runtime():
    path = ROOT / '.runtime/local.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def verify_resume(output,script,context):
    if json.loads((output/'script.json').read_text(encoding='utf-8')) != script:
        raise RuntimeError('Resume script differs; create a new take.')
    if not (output/'run-context.json').is_file() or json.loads((output/'run-context.json').read_text(encoding='utf-8'))!=context:
        raise RuntimeError('Resume profile/runtime differs or is unrecorded; create a new take.')
    if (output/'manifest.json').exists():
        raise RuntimeError('Take is already complete; use --transcribe-only if QA remains.')


def ffmpeg_path():
    available = shutil.which('ffmpeg')
    if available:
        return available
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def setup_imports(config):
    source = config.get('voice_source')
    if source:
        sys.path.insert(0, source)
        sys.path.insert(0, str(Path(source) / 'backend'))
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    os.environ.setdefault('HF_HOME', str(ROOT / '.runtime/huggingface'))
    os.environ.setdefault('TORCH_HOME', str(ROOT / '.runtime/torch'))
    os.environ.setdefault('AUDIOSEAL_CACHE_DIR', str(ROOT / '.runtime/models'))
    os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')
    # AudioSeal supports eager inference; avoid requiring a C++ toolchain.
    os.environ.setdefault('NO_TORCH_COMPILE', '1')


def choose_device(torch, requested):
    if requested != 'auto':
        return requested
    if torch.cuda.is_available():
        return 'cuda'
    if torch.backends.mps.is_available():
        return 'mps'
    return 'cpu'


def validate(items, profile):
    if not isinstance(items, list) or not items:
        raise ValueError('Script must be a non-empty array of passages.')
    seen = set()
    for index, item in enumerate(items):
        ident = item.get('id', '')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', ident) or ident in seen:
            raise ValueError(f'Invalid or duplicate passage id: {ident}')
        seen.add(ident)
        if not isinstance(item.get('text'), str) or not item['text'].strip():
            raise ValueError(f'Missing spoken text: {ident}')
        language = item.get('language', profile.get('language', 'en'))
        if not isinstance(language, str) or not re.fullmatch(r'[a-z]{2,3}', language):
            raise ValueError(f'Use an explicit lowercase language code for {ident}.')
        for key, default, low, high in [('speed', profile['speed'], .5, 1.5), ('pause_after', 0, 0, 3)]:
            item.setdefault(key, default)
            if not isinstance(item[key], (int, float)) or not math.isfinite(item[key]) or not low <= item[key] <= high:
                raise ValueError(f'Invalid {key} for {ident}')
        item.setdefault('seed', profile['seed'])
        if type(item['seed']) is not int or not 0 <= item['seed'] < 2**63:
            raise ValueError('Seed must be a nonnegative integer.')
    return items


def watermark(values, sample_rate, config):
    import torch
    if config.get('watermark') == 'voicestudio':
        from services.watermark import mark_synthetic
        return mark_synthetic(torch.as_tensor(values), sample_rate, context='academic_video_studio.production').detach().cpu().numpy()
    # The public AudioSeal package is used directly; VoiceStudio is not required.
    from audioseal import AudioSeal
    from torchaudio.functional import resample
    generator = AudioSeal.load_generator('audioseal_wm_16bits').cpu().eval()
    signal = torch.as_tensor(values, dtype=torch.float32).reshape(1, 1, -1)
    with torch.inference_mode():
        at16 = resample(signal, sample_rate, 16000) if sample_rate != 16000 else signal
        mark = generator.get_watermark(at16)
        if sample_rate != 16000:
            mark = resample(mark, 16000, sample_rate)
        mark = torch.nn.functional.pad(mark, (0, max(0, signal.shape[-1]-mark.shape[-1])))
        marked = signal + mark[..., :signal.shape[-1]]
    return marked.reshape(-1).numpy()


def transcribe(output, manifest, config):
    import numpy as np
    import soundfile as sf
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    import math as maths
    model_path = config.get('asr_dir') or str(ROOT / '.runtime/models/asr')
    asr = WhisperModel(model_path, device='cpu', compute_type='int8', cpu_threads=min(8, os.cpu_count() or 4), local_files_only=True)
    master, rate = sf.read(output / 'narration.wav', dtype='float32')
    captions, reports = [], []
    for scene in manifest['scenes']:
        values = master[scene['start_sample']:scene['end_sample']]
        if rate != 16000:
            gcd = maths.gcd(rate, 16000)
            values = resample_poly(values, 16000 // gcd, rate // gcd).astype(np.float32)
        language = scene.get('language', 'en')
        if language != 'en' and not asr.model.is_multilingual:
            raise ValueError('Non-English QA requires a multilingual Whisper model, not an English-only .en model.')
        segments, _ = asr.transcribe(values, language=language, beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
        recognised = []
        for segment in segments:
            recognised.append(segment.text.strip())
            for word in segment.words or []:
                start = round((scene['start_seconds'] + word.start) * 1000)
                end = round((scene['start_seconds'] + word.end) * 1000)
                captions.append({'text':word.word, 'startMs':start, 'endMs':end, 'timestampMs':round((start+end)/2), 'confidence':word.probability})
        heard = ' '.join(recognised)
        expected_tokens, actual_tokens = words(scene['text'],language), words(heard,language)
        matcher = difflib.SequenceMatcher(None, expected_tokens, actual_tokens, autojunk=False)
        reports.append({'id':scene['id'], 'language':language, 'intended':scene['text'], 'recognised':heard, 'similarity':matcher.ratio(), 'differences':[{'operation':op,'intended':expected_tokens[a:b],'recognised':actual_tokens[c:d]} for op,a,b,c,d in matcher.get_opcodes() if op != 'equal']})
        print(f"Transcript checked: {scene['id']} ({matcher.ratio():.3f})", flush=True)
    if not captions:
        raise RuntimeError('No speech recognised; audio is retained for diagnosis.')
    write_json(output/'captions.json', captions)
    write_json(output/'transcription-qa.json', {'audio_sha256':sha(output/'narration.wav'),'passages':reports,'note':'ASR flags are review candidates, not proof of pronunciation or accent. Never cut audio at these word boundaries.'})
    def stamp(ms):
        seconds, millis = divmod(ms, 1000); minutes, seconds = divmod(seconds,60); hours, minutes = divmod(minutes,60)
        return f'{hours:02}:{minutes:02}:{seconds:02},{millis:03}'
    groups, group = [], []
    for word in captions:
        if group and (len(group)>=8 or word['endMs']-group[0]['startMs']>3800):
            groups.append(group); group=[]
        group.append(word)
        if word['text'].rstrip().endswith(('.', '?', '!')):
            groups.append(group); group=[]
    if group: groups.append(group)
    with (output/'captions.srt').open('x', encoding='utf-8') as stream:
        for index, group in enumerate(groups,1):
            stream.write(f"{index}\n{stamp(group[0]['startMs'])} --> {stamp(group[-1]['endMs'])}\n{''.join(w['text'] for w in group).strip()}\n\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--device', choices=['auto','cuda','mps','cpu'], default='auto')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--no-transcribe', action='store_true')
    parser.add_argument('--transcribe-only', action='store_true')
    args = parser.parse_args()
    config = runtime(); setup_imports(config)
    if args.transcribe_only:
        if args.output is None:parser.error('--output is required')
        output=args.output.resolve()
        manifest=json.loads((output/'manifest.json').read_text(encoding='utf-8'))
        if sha(output/'narration.wav') != manifest['narration_sha256']:
            raise RuntimeError('Narration hash does not match the manifest.')
        transcribe(output,manifest,config); return
    args.profile=(args.profile or Path(config.get('profile','voices/local/profile.json')))
    if not args.profile.is_absolute(): args.profile=ROOT/args.profile
    if not args.profile.is_file():
        parser.error('No voice profile registered. Follow docs/VOICE.md or supply --profile.')
    profile = json.loads(args.profile.read_text(encoding='utf-8'))
    reference = args.profile.parent/profile['reference_audio']
    reference_text = args.profile.parent/profile['reference_text']
    if sha(reference) != profile['reference_sha256']:
        raise RuntimeError('Human reference hash changed. Review the new reference explicitly.')
    if sha(reference_text) != profile['reference_text_sha256']:
        raise RuntimeError('Reference transcript changed. Register a new reviewed profile.')
    import numpy as np
    import soundfile as sf
    import torch
    from omnivoice import OmniVoice
    device = choose_device(torch, args.device)
    model_path = config.get('model_dir') or str(ROOT/'.runtime/models/omnivoice')
    if args.check:
        print(json.dumps({'voice':profile['name'],'reference_verified':True,'device':device,'model_present':Path(model_path).is_dir(),'python':sys.executable,'torch':torch.__version__,'ffmpeg':ffmpeg_path()},indent=2)); return
    if args.output is None:
        parser.error('--output is required')
    output = args.output.resolve()
    if args.script is None:
        parser.error('--script is required')
    script = validate(json.loads(args.script.read_text(encoding='utf-8-sig')), profile)
    context={'profile_sha256':sha(args.profile),'reference_sha256':sha(reference),
             'reference_text_sha256':sha(reference_text),'device':device,'torch':torch.__version__,
             'model_dir':str(model_path),'generation':profile['generation']}
    if output.exists():
        if not args.resume:
            raise FileExistsError('Take exists. Use a new take folder or --resume for the identical script.')
        verify_resume(output,script,context)
    else:
        output.mkdir(parents=True); (output/'scenes').mkdir(); write_json(output/'script.json',script)
        write_json(output/'run-context.json',context)
    # Stable Apple Silicon route. Audio tokenizer is handled on CPU by OmniVoice.
    dtype=torch.float16 if device=='cuda' else torch.float32
    options={'device_map':device,'dtype':dtype,'load_asr':False,'local_files_only':True}
    if device=='mps': options['attn_implementation']='eager'
    print(f"Loading {profile['name']} voice on {device}; {dtype}.",flush=True)
    model=OmniVoice.from_pretrained(model_path,**options)
    prompt=model.create_voice_clone_prompt(ref_audio=str(reference),ref_text=(args.profile.parent/profile['reference_text']).read_text(encoding='utf-8').strip(),preprocess_prompt=True)
    rate=model.sampling_rate; arrays=[]; cursor=0; scenes=[]
    for index,item in enumerate(script):
        filename=f"{index+1:02}-{item['id']}.wav"; path=output/'scenes'/filename; record_path=path.with_suffix('.json')
        started=time.perf_counter()
        if path.exists():
            if not args.resume or not record_path.exists():
                raise RuntimeError(f'Unverified existing take {path}; preserve and start a new take.')
            record=json.loads(record_path.read_text(encoding='utf-8'))
            if sha(path)!=record['sha256']:raise RuntimeError('Existing scene hash changed.')
            values,old_rate=sf.read(path,dtype='float32');assert old_rate==rate
        else:
            torch.manual_seed(item['seed'])
            if device=='cuda':torch.cuda.manual_seed_all(item['seed'])
            with torch.inference_mode():
                generated=model.generate(text=item.get('tts_text',item['text']),language=item.get('language',profile.get('language','en')),voice_clone_prompt=prompt,speed=item['speed'],**profile['generation'])[0]
            values=generated.detach().cpu().numpy() if hasattr(generated,'detach') else np.asarray(generated)
            values=np.asarray(values,dtype=np.float32).reshape(-1)
            if not len(values) or not np.isfinite(values).all() or np.max(np.abs(values))<1e-5:
                raise RuntimeError('Silent or non-finite generation. Retain this take and retry a new take/device.')
            values=np.asarray(watermark(values,rate,config),dtype=np.float32).reshape(-1)
            with path.open('xb') as stream:sf.write(stream,values,rate,format='WAV',subtype='PCM_16')
            record={'sha256':sha(path),'generation_seconds':time.perf_counter()-started,'synthetic':True}
            write_json(record_path,record)
            values,_=sf.read(path,dtype='float32')
        end=cursor+len(values)
        scenes.append({**item,'language':item.get('language',profile.get('language','en')),'file':'scenes/'+filename,'sha256':sha(path),'start_sample':cursor,'end_sample':end,'start_seconds':cursor/rate,'end_seconds':end/rate,'duration_seconds':len(values)/rate,'prosody':item.get('prosody',{})})
        arrays.append(values);cursor=end
        padding=round(item['pause_after']*rate)
        if padding:arrays.append(np.zeros(padding,dtype=np.float32));cursor+=padding
        print(f"{index+1}/{len(script)} {item['id']}: {len(values)/rate:.2f}s",flush=True)
    with (output/'narration-raw.wav').open('xb') as stream:sf.write(stream,np.concatenate(arrays),rate,format='WAV',subtype='PCM_16')
    subprocess.run([ffmpeg_path(),'-hide_banner','-loglevel','error','-nostdin','-n','-i',str(output/'narration-raw.wav'),'-af','loudnorm=I=-18:TP=-1.5:LRA=9','-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(output/'narration.wav')],check=True)
    info=sf.info(output/'narration.wav')
    if abs(info.duration-cursor/rate)>.001:raise RuntimeError('Mastering unexpectedly changed duration.')
    manifest={'voice':profile['name'],'profile_sha256':sha(args.profile),'reference_sha256':sha(reference),'sample_rate':rate,'duration_seconds':info.duration,'narration_sha256':sha(output/'narration.wav'),'device':device,'dtype':str(dtype),'generation':profile['generation'],'synthetic':True,'scenes':scenes}
    write_json(output/'manifest.json',manifest)
    del model,prompt
    if device=='cuda':torch.cuda.empty_cache()
    if device=='mps':torch.mps.empty_cache()
    if not args.no_transcribe:transcribe(output,manifest,config)
    print(f'Complete: {output / "narration.wav"}',flush=True)


if __name__=='__main__':
    if sys.stdout is not None:sys.stdout.reconfigure(encoding='utf-8')
    main()
