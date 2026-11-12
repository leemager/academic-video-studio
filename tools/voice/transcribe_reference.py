"""Transcribe an original voice recording locally before registering its profile."""
import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASR_REPO = 'Systran/faster-whisper-small'
ASR_REVISION = '536b0662742c02347bc0e980a01041f333bce120'


def transcribe_reference(audio, output, language=None, model_dir=None):
    audio, output = Path(audio).resolve(), Path(output).resolve()
    report_path = output.with_suffix('.asr.json')
    if not audio.is_file():
        raise FileNotFoundError(f'Recording not found: {audio}')
    if output.suffix.lower() != '.txt':
        raise ValueError('Use a .txt output filename.')
    if output.exists() or report_path.exists():
        raise FileExistsError('Transcript already exists. Keep it and choose a new output filename.')

    config_path = ROOT / '.runtime/local.json'
    config = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    selected = model_dir or config.get('asr_dir')
    model_path = Path(selected).resolve() if selected else ROOT / '.runtime/models/asr'
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError('Install the local transcription tools using docs/VOICE.md, then retry.') from exc
    if not (model_path / 'model.bin').is_file():
        if selected:
            raise FileNotFoundError(f'Whisper model is missing at {model_path}. Check setup or --model-dir.')
        from huggingface_hub import snapshot_download
        print('Downloading the local transcription model...', flush=True)
        snapshot_download(repo_id=ASR_REPO, revision=ASR_REVISION, local_dir=str(model_path))

    source_hash = hashlib.sha256(audio.read_bytes()).hexdigest()
    model = WhisperModel(str(model_path), device='cpu', compute_type='int8',
                         cpu_threads=min(8, os.cpu_count() or 4), local_files_only=True)
    if language and language != 'en' and not model.model.is_multilingual:
        raise ValueError('Use a multilingual Whisper model for a non-English recording.')
    segments, info = model.transcribe(str(audio), language=language, task='transcribe',
                                     beam_size=5, word_timestamps=True, vad_filter=False,
                                     condition_on_previous_text=False)
    records = []
    for segment in segments:
        records.append({
            'start': segment.start, 'end': segment.end, 'text': segment.text,
            'words': [{'text': w.word, 'start': w.start, 'end': w.end,
                       'probability': w.probability} for w in segment.words or []],
        })
    text = ''.join(segment['text'] for segment in records).strip()
    if not text:
        raise RuntimeError('No speech recognised. Check the recording before registering the voice.')
    report = {'audio': audio.name, 'audio_sha256': source_hash,
              'language': info.language, 'language_probability': info.language_probability,
              'segments': records}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        stream.write(text + '\n')
    with report_path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    return {'transcript': str(output), 'details': str(report_path),
            'language': info.language, 'text': text}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--language', help='Known language code; otherwise detect it from the recording.')
    parser.add_argument('--model-dir', type=Path, help='Use an existing local Whisper model.')
    args = parser.parse_args()
    print(json.dumps(transcribe_reference(args.audio, args.output, args.language, args.model_dir),
                     indent=2, ensure_ascii=False))
