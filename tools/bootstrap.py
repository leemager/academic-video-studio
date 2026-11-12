"""Install repository-local tools. Standard-library Python 3.9+ is enough to start.

Uses official Node and uv downloads with SHA256 verification. No sudo, Homebrew,
global PATH edits, deleting existing environments, or cloud voice service.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
RUNTIME=ROOT/'.runtime'
NODE_VERSION='24.15.0'
UV_VERSION='0.8.22'


def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'AcademicVideoStudio/1.0'})
    with urllib.request.urlopen(request,timeout=180) as response:return response.read()


def safe_unpack(archive,destination):
    destination=destination.resolve();destination.mkdir(parents=True,exist_ok=True)
    if archive.suffix=='.zip':
        with zipfile.ZipFile(archive) as bundle:
            for item in bundle.infolist():
                target=(destination/item.filename).resolve()
                if not target.is_relative_to(destination):raise ValueError('Archive path escapes target.')
                mode=item.external_attr>>16
                if (mode&0o170000)==0o120000:raise ValueError('Archive contains a symlink.')
            bundle.extractall(destination)
    else:
        with tarfile.open(archive) as bundle:
            # Official Node archives contain npm/npx symlinks; copy regular files
            # only and call npm-cli.js with Node directly below.
            members=[]
            for member in bundle.getmembers():
                target=(destination/member.name).resolve()
                if not target.is_relative_to(destination):raise ValueError('Archive path escapes target.')
                if member.isfile() or member.isdir():members.append(member)
            bundle.extractall(destination,members=members)


def install_archive(url,checksum_url,name,folder,checksum=None):
    downloads=RUNTIME/'downloads';downloads.mkdir(parents=True,exist_ok=True)
    archive=downloads/name
    if checksum is None:
        manifest=fetch(checksum_url).decode()
        entries=[line.split()[0] for line in manifest.splitlines() if name in line]
        checksum=entries[0] if entries else manifest.split()[0]
    if not archive.exists():
        print('Downloading '+name,flush=True)
        with archive.open('xb') as stream:stream.write(fetch(url))
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=checksum:
        raise RuntimeError(f'Checksum mismatch; retained {archive}. Do not use it.')
    if not folder.exists():safe_unpack(archive,folder)
    return folder


def node_tools(system,machine):
    suffix={'Darwin':'darwin','Windows':'win','Linux':'linux'}[system]
    arch='arm64' if machine in ('arm64','aarch64') else 'x64'
    stem=f'node-v{NODE_VERSION}-{suffix}-{arch}'
    name=stem+('.zip' if system=='Windows' else '.tar.gz')
    folder=install_archive(f'https://nodejs.org/dist/v{NODE_VERSION}/{name}',f'https://nodejs.org/dist/v{NODE_VERSION}/SHASUMS256.txt',name,RUNTIME/'node')/stem
    if system=='Windows':return folder/'node.exe',folder/'node_modules/npm/bin/npm-cli.js'
    return folder/'bin/node',folder/'lib/node_modules/npm/bin/npm-cli.js'


def uv_tool(system,machine):
    arch='aarch64' if machine in ('arm64','aarch64') else 'x86_64'
    target={'Darwin':'apple-darwin','Windows':'pc-windows-msvc','Linux':'unknown-linux-gnu'}[system]
    name=f'uv-{arch}-{target}'+('.zip' if system=='Windows' else '.tar.gz')
    base=f'https://github.com/astral-sh/uv/releases/download/{UV_VERSION}/'
    folder=install_archive(base+name,base+name+'.sha256',name,RUNTIME/'uv')
    matches=list(folder.rglob('uv.exe' if system=='Windows' else 'uv'))
    matches=[p for p in matches if p.is_file()]
    if len(matches)!=1:raise RuntimeError('Cannot locate the verified uv executable.')
    return matches[0]


def platform_plan(system,machine,preview_only=False,backend='auto',nvidia=False):
    if system not in ('Darwin','Windows','Linux'):
        raise ValueError('Unsupported operating system.')
    machine=machine.lower()
    if machine not in ('arm64','aarch64','x64','x86_64','amd64'):
        raise ValueError('Only 64-bit x64/ARM tool downloads are available.')
    arm=machine in ('arm64','aarch64')
    supported=(system=='Darwin' and arm) or (system in ('Windows','Linux') and not arm)
    selected=('mps' if system=='Darwin' and arm else 'cuda' if nvidia else 'cpu') if backend=='auto' else backend
    if selected=='cuda' and (system=='Darwin' or arm):
        raise ValueError('This starter supports CUDA on Windows/Linux x64 only.')
    return {'platform':system,'architecture':machine,'node':NODE_VERSION,'uv':UV_VERSION,'python':'3.11',
            'voice_install':supported and not preview_only,'torch_backend':selected,
            'model_downloads':'OmniVoice, multilingual Whisper small, tokenizer and AudioSeal; several GB',
            'scope':'Repository-local tools and weights; no voice upload or paid API.',
            'voice_limit':None if supported else 'This architecture is not supported by the pinned local voice stack. Preview/render and imported audio remain available where the browser runs.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-only',action='store_true')
    parser.add_argument('--audio-only',action='store_true',help='Install lightweight import/registration utilities without a TTS model.')
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--torch-backend',choices=['auto','cpu','cuda'],default='auto')
    args=parser.parse_args();system=platform.system();machine=platform.machine().lower()
    nvidia=False
    if shutil.which('nvidia-smi'):
        nvidia=subprocess.run(['nvidia-smi','-L'],capture_output=True).returncode==0
    plan=platform_plan(system,machine,args.preview_only,args.torch_backend,nvidia)
    if args.audio_only:plan['voice_install']=False
    plan['audio_install']=not args.preview_only and (args.audio_only or (system=='Darwin' and machine not in ('arm64','aarch64')))
    print(json.dumps(plan,indent=2),flush=True)
    if args.dry_run:return
    RUNTIME.mkdir(exist_ok=True)
    config_path=RUNTIME/'local.json'
    config=json.loads(config_path.read_text()) if config_path.exists() else {}
    node,npm=node_tools(system,machine)
    env=dict(os.environ,PATH=str(node.parent)+os.pathsep+os.environ.get('PATH',''),UV_PYTHON_INSTALL_DIR=str(RUNTIME/'python'),UV_PYTHON_BIN_DIR=str(RUNTIME/'python-bin'),UV_CACHE_DIR=str(RUNTIME/'uv-cache'),HF_HOME=str(RUNTIME/'huggingface'),TORCH_HOME=str(RUNTIME/'torch'))
    # npm install is repeatable and preserves existing files; npm ci would remove node_modules.
    subprocess.run([str(node),str(npm),'install','--no-fund'],cwd=ROOT,env=env,check=True)
    subprocess.run([str(node),str(ROOT/'node_modules/@remotion/cli/remotion-cli.js'),'browser','ensure'],cwd=ROOT,env=env,check=True)
    config.update(node=str(node),npm=str(npm))
    if plan['voice_install']:
        uv=uv_tool(system,machine)
        subprocess.run([str(uv),'python','install','3.11','--no-bin','--no-registry'],env=env,check=True)
        venv=ROOT/'.venv'
        if not venv.exists():subprocess.run([str(uv),'venv','--python','3.11',str(venv)],env=env,check=True)
        python=venv/('Scripts/python.exe' if system=='Windows' else 'bin/python')
        if system in ('Windows','Linux'):
            index='https://download.pytorch.org/whl/'+('cu128' if plan['torch_backend']=='cuda' else 'cpu')
            subprocess.run([str(uv),'pip','install','--python',str(python),'torch==2.8.0','torchaudio==2.8.0','--index-url',index],env=env,check=True)
        requirements=ROOT/('requirements-macos-lock.txt' if system=='Darwin' else 'requirements-voice.txt')
        subprocess.run([str(uv),'pip','install','--python',str(python),'-r',str(requirements)],env=env,check=True)
        config.update(python=str(python),model_dir=str(RUNTIME/'models/omnivoice'),asr_dir=str(RUNTIME/'models/asr'),watermark='audioseal',mode='voice')
        config.pop('voice_source',None)
        subprocess.run([str(python),str(ROOT/'tools/voice/download-models.py')],env=env,check=True)
    elif plan['audio_install']:
        uv=uv_tool(system,machine)
        subprocess.run([str(uv),'python','install','3.11','--no-bin','--no-registry'],env=env,check=True)
        venv=ROOT/'.venv-audio'
        if not venv.exists():subprocess.run([str(uv),'venv','--python','3.11',str(venv)],env=env,check=True)
        python=venv/('Scripts/python.exe' if system=='Windows' else 'bin/python')
        subprocess.run([str(uv),'pip','install','--python',str(python),'-r',str(ROOT/'requirements-audio.txt')],env=env,check=True)
        config.update(python=str(python),mode='audio')
        print('Audio import/registration ready; no local TTS or ASR models installed.',flush=True)
        if plan['voice_limit']:print(plan['voice_limit'],flush=True)
    else:
        print('Preview and rendering are ready. Voice installation was skipped.',flush=True)
        if plan['voice_limit']:print(plan['voice_limit'],flush=True)
    if config_path.exists():
        backup=RUNTIME/('local-before-setup-'+__import__('datetime').datetime.now().strftime('%Y%m%d-%H%M%S')+'.json')
        shutil.copy2(config_path,backup)
    config_path.write_text(json.dumps(config,indent=2)+'\n')
    subprocess.run([str(node),str(ROOT/'tools/doctor.mjs')],cwd=ROOT,env=env,check=True)
    print('Setup complete. Open StarterDemo, then register your own voice using docs/VOICE.md.',flush=True)


if __name__=='__main__':main()
