"""Apply whole-passage selections to a new take, preserving every selected sample."""
import argparse,json,shutil,subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
from render import ROOT,sha,write_json,ffmpeg_path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--selection',action='append',type=Path,default=[]);a=p.parse_args()
base=json.loads((a.base/'manifest.json').read_text(encoding='utf-8')); selections={}
for path in a.selection:
 s=json.loads(path.read_text(encoding='utf-8'));file=(ROOT/s['file']).resolve()
 if not file.is_relative_to(ROOT) or sha(file)!=s['sha256']:raise RuntimeError('Selection file/hash mismatch.')
 if s['passageId'] in selections:raise RuntimeError('Conflicting selections for one passage.')
 selections[s['passageId']]=s
if set(selections)-{s['id'] for s in base['scenes']}:raise RuntimeError('Selection is not part of this project.')
a.output.mkdir(parents=True);(a.output/'scenes').mkdir();arrays=[];cursor=0;scenes=[];rate=base['sample_rate']
for scene in base['scenes']:
 chosen=selections.get(scene['id']);source=ROOT/chosen['file'] if chosen else a.base/scene['file'];expected=chosen['sha256'] if chosen else scene['sha256']
 if sha(source)!=expected:raise RuntimeError('Source audio changed.')
 if chosen and chosen['text']!=scene['text']:raise RuntimeError('Text changed: update the reviewed script explicitly, then create a new narration take.')
 values,sr=sf.read(source,dtype='float32')
 if sr!=rate or values.ndim!=1:raise RuntimeError('Selected passage sample format differs; do not silently resample.')
 target=a.output/scene['file'];shutil.copy2(source,target)
 end=cursor+len(values);new_scene={**scene,'sha256':expected,'start_sample':cursor,'end_sample':end,'start_seconds':cursor/rate,'end_seconds':end/rate,'duration_seconds':len(values)/rate}
 if chosen:
  for key in ('seed','speed','tts_text'):new_scene.pop(key,None)
  new_scene['replacement_provenance']=chosen
 scenes.append(new_scene)
 arrays.append(values);cursor=end;padding=round(scene.get('pause_after',0)*rate)
 if padding:arrays.append(np.zeros(padding,dtype='float32'));cursor+=padding
with (a.output/'narration-raw.wav').open('xb') as stream:sf.write(stream,np.concatenate(arrays),rate,format='WAV',subtype='PCM_16')
subprocess.run([ffmpeg_path(),'-hide_banner','-loglevel','error','-nostdin','-n','-i',str(a.output/'narration-raw.wav'),'-af','loudnorm=I=-18:TP=-1.5:LRA=9','-ar',str(rate),'-ac','1','-c:a','pcm_s16le',str(a.output/'narration.wav')],check=True)
if abs(sf.info(a.output/'narration.wav').duration-cursor/rate)>.001:raise RuntimeError('Master duration changed.')
write_json(a.output/'manifest.json',{**base,'scenes':scenes,'duration_seconds':cursor/rate,'narration_sha256':sha(a.output/'narration.wav'),'applied_selections':selections})
print(a.output)
