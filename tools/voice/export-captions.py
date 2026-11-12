"""Source-text captions timed from verified passage ASR, with an explicit video offset.

Spelling comes from the academic script. Word timing is approximate, especially
where number/name tokenisation differs. This never modifies or cuts audio.
"""
import argparse,difflib,json,re,textwrap
from pathlib import Path
from render import sha,write_json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--take',type=Path,required=True);p.add_argument('--alignment',type=Path,action='append',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--offset',type=float,default=2);a=p.parse_args()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
target=read(a.take/'manifest.json');alignments={}
for folder in a.alignment:
 m=read(folder/'manifest.json');words=read(folder/'captions.json');qa=read(folder/'transcription-qa.json')
 if sha(folder/'narration.wav')!=m['narration_sha256'] or qa['audio_sha256']!=m['narration_sha256']:raise RuntimeError('ASR master hash mismatch.')
 for s in m['scenes']:
  if sha(folder/s['file'])!=s['sha256']:raise RuntimeError('ASR passage hash mismatch.')
  alignments[s['sha256']]=(s,[w for w in words if s['start_seconds']*1000-1<=w['startMs']<s['end_seconds']*1000])
def norm(t):return re.sub(r'[^\w]','',t.casefold())
all_words=[];uncertain=[]
for scene in target['scenes']:
 old,actual=alignments[scene['sha256']];expected=re.findall(r'\S+',scene['text'])
 matcher=difflib.SequenceMatcher(None,[norm(w) for w in expected],[norm(w['text']) for w in actual],autojunk=False)
 mapped=[]
 for op,i,j,k,l in matcher.get_opcodes():
  if i==j:continue
  if op=='equal':
   mapped.extend({'text':t,'startMs':actual[k+n]['startMs'],'endMs':actual[k+n]['endMs']} for n,t in enumerate(expected[i:j]))
  else:
   start=actual[k]['startMs'] if k<len(actual) else (actual[-1]['endMs'] if actual else old['start_seconds']*1000)
   end=actual[l-1]['endMs'] if l>k else min(start+150*(j-i),old['end_seconds']*1000)
   weights=[max(1,len(norm(t))) for t in expected[i:j]];cursor=start;total=sum(weights)
   for t,w in zip(expected[i:j],weights):
    next_time=cursor+(end-start)*w/total;mapped.append({'text':t,'startMs':cursor,'endMs':next_time});cursor=next_time
   uncertain.append({'scene':scene['id'],'operation':op,'source':expected[i:j],'recognised':[w['text'] for w in actual[k:l]]})
 delta=(scene['start_seconds']-old['start_seconds']+a.offset)*1000
 all_words.extend({**w,'startMs':round(w['startMs']+delta),'endMs':round(w['endMs']+delta)} for w in mapped)
def stamp(ms):
 seconds,millis=divmod(max(0,round(ms)),1000);minutes,seconds=divmod(seconds,60);hours,minutes=divmod(minutes,60)
 return f'{hours:02}:{minutes:02}:{seconds:02},{millis:03}'
groups=[];group=[]
for word in all_words:
 if group and (len(group)>=9 or len(' '.join(w['text'] for w in group))+len(word['text'])>76 or word['endMs']-group[0]['startMs']>4500):groups.append(group);group=[]
 group.append(word)
 if word['text'].endswith(('.', '?','!')) and len(group)>3:groups.append(group);group=[]
if group:groups.append(group)
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('x',encoding='utf-8') as stream:
 for i,group in enumerate(groups,1):
  end=min(group[-1]['endMs'],groups[i][0]['startMs']-1) if i<len(groups) else group[-1]['endMs']
  stream.write(f"{i}\n{stamp(group[0]['startMs'])} --> {stamp(max(group[0]['startMs']+1,end))}\n"+textwrap.fill(' '.join(w['text'] for w in group),width=44)+'\n\n')
write_json(a.output.with_suffix('.alignment.json'),{'narration_sha256':target['narration_sha256'],'video_offset_seconds':a.offset,'source_word_count':len(all_words),'approximate_spans':uncertain,'note':'Source spelling preserved; timings interpolated where ASR tokenisation differs. Not pronunciation verification.'})
write_json(a.output.with_suffix('.words.json'),all_words)
print(a.output)
