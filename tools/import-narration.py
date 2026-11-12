"""Import complete human/VoiceStudio passages without loading a voice model."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import numpy as np
import soundfile as sf
import imageio_ffmpeg


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,value):
    with p.open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,ensure_ascii=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--script',type=Path,required=True);p.add_argument('--files',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--synthetic',action='store_true')
    a=p.parse_args();script=read(a.script);files=read(a.files)
    if not isinstance(script,list) or not script:raise ValueError('Script must contain passages.')
    ids=[s.get('id') for s in script]
    if len(set(ids))!=len(ids) or any(not isinstance(i,str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',i) for i in ids):raise ValueError('Invalid/duplicate passage IDs.')
    if any(not isinstance(s.get('text'),str) or not s['text'].strip() for s in script):raise ValueError('Script text required.')
    if [s.get('id') for s in files]!=ids:raise ValueError('Import IDs/order must exactly match script.')
    sources=[Path(s['file']).resolve() for s in files]
    if any(not f.is_file() for f in sources):raise ValueError('An input recording is missing.')
    a.output.mkdir(parents=True);(a.output/'originals').mkdir();(a.output/'scenes').mkdir()
    write(a.output/'script.json',script)
    arrays=[];scenes=[];cursor=0;rate=24000
    for i,(scene,source) in enumerate(zip(script,sources)):
        original=a.output/'originals'/f'{i+1:02}-{scene["id"]}{source.suffix.lower()}'
        shutil.copy2(source,original)
        target=a.output/'scenes'/f'{i+1:02}-{scene["id"]}.wav'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-nostdin','-n','-i',str(original),'-vn','-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(target)],check=True)
        values,sr=sf.read(target,dtype='float32')
        if not len(values) or sr!=rate or not np.isfinite(values).all() or np.max(np.abs(values))<1e-5:raise ValueError('Imported passage is silent or invalid; retained for diagnosis.')
        end=cursor+len(values)
        scenes.append({'id':scene['id'],'text':scene['text'],'language':scene.get('language','en'),'file':target.relative_to(a.output).as_posix(),'sha256':sha(target),'start_sample':cursor,'end_sample':end,'start_seconds':cursor/rate,'end_seconds':end/rate,'duration_seconds':len(values)/rate,'pause_after':0,'original_sha256':sha(original),'synthetic':a.synthetic})
        arrays.append(values);cursor=end
    with (a.output/'narration-raw.wav').open('xb') as stream:sf.write(stream,np.concatenate(arrays),rate,format='WAV',subtype='PCM_16')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-nostdin','-n','-i',str(a.output/'narration-raw.wav'),'-af','loudnorm=I=-18:TP=-1.5:LRA=9','-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(a.output/'narration.wav')],check=True)
    if abs(sf.info(a.output/'narration.wav').duration-cursor/rate)>.001:raise ValueError('Master duration changed.')
    write(a.output/'manifest.json',{'voice':'Imported narration','reference_sha256':None,'sample_rate':rate,'duration_seconds':cursor/rate,'narration_sha256':sha(a.output/'narration.wav'),'synthetic':a.synthetic,'scenes':scenes,'note':'Whole-passage format conversion; original sources preserved. Import does not establish a voice-clone reference.'})
    print(a.output/'narration.wav')


if __name__=='__main__':main()
