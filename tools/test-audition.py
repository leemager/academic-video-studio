"""Exercise the loopback audition protocol with synthetic tones, not a person's voice."""
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time
import urllib.error
import urllib.request
import uuid
import wave

ROOT=Path(__file__).resolve().parents[1]
slug='protocol-test-'+uuid.uuid4().hex[:10]
folder=ROOT/'.work'/slug;folder.mkdir(parents=True)
wav=folder/'signal.wav'
with wave.open(str(wav),'wb') as w:
    w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(b'\0\0'*2400)
spec={'slug':slug,'title':'Automated protocol test','text':'Silent fixture; not a voice audition.','passageId':'fixture','takes':[{'file':str(wav),'label':'Test fixture'}]}
source=folder/'spec.json';source.write_text(json.dumps(spec),encoding='utf-8')
local=json.loads((ROOT/'.runtime/local.json').read_text(encoding='utf-8'))
node=local.get('node','node')
subprocess.run([node,'tools/create-audition.mjs',str(source)],cwd=ROOT,check=True)
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
server=subprocess.Popen([node,'tools/auditions.mjs',slug],cwd=ROOT,env={**os.environ,'AUDITION_PORT':str(port)},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
base=f'http://127.0.0.1:{port}'
try:
    for _ in range(50):
        try:html=urllib.request.urlopen(base).read().decode();break
        except urllib.error.URLError:time.sleep(.1)
    else:raise RuntimeError('Audition server did not start.')
    token=re.search(r"const token='([^']+)'",html)[1]
    manifest=json.loads(urllib.request.urlopen(base+'/manifest').read())
    take=manifest['takes'][0]
    response=urllib.request.urlopen(base+'/audio/'+take['file'])
    assert response.headers['Cache-Control']=='no-store'
    assert hashlib.sha256(response.read()).hexdigest()==take['sha256']
    partial=urllib.request.urlopen(urllib.request.Request(base+'/audio/'+take['file'],headers={'Range':'bytes=0-9'}))
    assert partial.status==206 and len(partial.read())==10
    def choose(token):
        return urllib.request.urlopen(urllib.request.Request(base+'/choose',data=b'{"id":"A"}',headers={'Content-Type':'application/json','Origin':base,'X-Audition-Token':token}))
    try:choose('wrong')
    except urllib.error.HTTPError as e:assert e.code==403
    else:raise AssertionError('Selection accepted without valid token')
    saved=json.loads(choose(token).read())
    selection=json.loads((ROOT/saved['saved']).read_text(encoding='utf-8'))
    assert selection['sha256']==take['sha256'] and selection['passageId']=='fixture'
    print('PASS: audition creation, audio hash, no-cache, range playback, token rejection and selected-waveform record.')
    print('Task-owned fixtures retained under .work/, public/auditions/ and voiceover/selections/.')
finally:
    server.terminate();server.wait(timeout=10)
