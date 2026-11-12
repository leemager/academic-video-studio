"""Register an original human recording locally; never trains on generated audio."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def register(audio, transcript, name, slug='local', language='en', source='Original recording supplied by speaker'):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', slug):
        raise ValueError('Use a simple lowercase voice identifier.')
    if not re.fullmatch(r'[a-z]{2,3}', language):
        raise ValueError('Use a lowercase language code such as en, fr or zh.')
    if not name.strip():
        raise ValueError('A speaker name is required.')
    audio, transcript = Path(audio).resolve(), Path(transcript).resolve()
    if not audio.is_file() or not transcript.is_file():
        raise ValueError('Supply an existing original recording and transcript file.')
    text = transcript.read_text(encoding='utf-8-sig').strip()
    if not text:
        raise ValueError('The transcript must contain the words actually spoken.')
    target = ROOT/'voices'/slug
    if target.exists():
        raise FileExistsError('Voice already exists. Use a new identifier; preserve the original profile.')
    if not (ROOT/'voices').resolve().is_relative_to(ROOT):
        raise ValueError('Voice folder must remain in the project.')
    import soundfile as sf
    import numpy as np
    import imageio_ffmpeg
    target.mkdir(parents=True)
    original = target/('original'+audio.suffix.lower())
    shutil.copy2(audio, original)
    shutil.copy2(transcript, target/'original-transcript.txt')
    reference = target/'reference.wav'
    # Whole-file format conversion only: no silence removal, denoising or cuts.
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-nostdin', '-n',
                    '-i', str(original), '-vn', '-ar', '24000', '-ac', '1', '-c:a', 'pcm_s16le', str(reference)], check=True)
    values, rate = sf.read(reference)
    duration = len(values)/rate
    if not 3 <= duration <= 60 or not np.isfinite(values).all() or np.max(np.abs(values)) < 1e-4:
        raise ValueError('Reference must contain audible speech, 3–60 seconds. Files retained; use a new voice folder after checking.')
    (target/'reference.txt').write_text(text+'\n', encoding='utf-8')
    profile = {
        'name':name.strip(), 'language':language, 'created':datetime.date.today().isoformat(),
        'reference_audio':'reference.wav', 'reference_text':'reference.txt',
        'reference_sha256':sha(reference), 'reference_text_sha256':sha(target/'reference.txt'),
        'seed':42, 'speed':1.0,
        'generation':{'num_step':32,'guidance_scale':2.0,'position_temperature':5.0,
                      'class_temperature':0.5,'denoise':True,'preprocess_prompt':True,'postprocess_output':True},
        'approval':'Original human reference registered by user direction; generated voice quality awaits listening review.',
        'provenance':{'source':source,'original_sha256':sha(original),'reference_seconds':duration,
                      'conversion':'Whole recording to mono 24kHz PCM16; no timing edits'},
    }
    (target/'profile.json').write_text(json.dumps(profile, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (target/'preferences.json').write_text(json.dumps({'speaker':name,'preferences':[]},indent=2)+'\n',encoding='utf-8')
    return {'profile':str(target/'profile.json'),'seconds':duration,'peak':float(np.max(np.abs(values))),
            'note':'Check transcript and voice identity with a short benchmark. These files are ignored by Git.'}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audio',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True)
    p.add_argument('--name',required=True);p.add_argument('--id',default='local');p.add_argument('--language',default='en')
    p.add_argument('--source',default='Original recording supplied by speaker')
    a=p.parse_args()
    print(json.dumps(register(a.audio,a.transcript,a.name,a.id,a.language,a.source),indent=2,ensure_ascii=False))
