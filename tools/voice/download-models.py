"""Explicit setup step: download public models, never upload voice samples."""
import os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ.setdefault('HF_HOME',str(ROOT/'.runtime/huggingface'))
os.environ.setdefault('TORCH_HOME',str(ROOT/'.runtime/torch'))
os.environ.setdefault('AUDIOSEAL_CACHE_DIR',str(ROOT/'.runtime/models'))
from huggingface_hub import snapshot_download
MODELS=[('k2-fsa/OmniVoice','c5fdb5ccb189668d56333f77ba2629f4cd7535f4','omnivoice'),('Systran/faster-whisper-small','536b0662742c02347bc0e980a01041f333bce120','asr')]
for repo,revision,name in MODELS:
    print('Downloading '+repo,flush=True)
    snapshot_download(repo_id=repo,revision=revision,local_dir=str(ROOT/'.runtime/models'/name))
from audioseal import AudioSeal
AudioSeal.load_generator('audioseal_wm_16bits')
print('Local voice, transcription and watermark models ready.')
