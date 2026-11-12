import {existsSync,readFileSync,statfsSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import os from 'node:os';
import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const p=path.join(root,'.runtime/local.json');
const local=existsSync(p)?JSON.parse(readFileSync(p,'utf8')):{};
const python=local.python||path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
const disk=statfsSync(root);
const profile=local.profile||'voices/local/profile.json';
const report={platform:process.platform,architecture:process.arch,memoryGB:Math.round(os.totalmem()/1024**3),freeDiskGB:Math.round(disk.bavail*disk.bsize/1024**3),node:process.version,remotion:existsSync(path.join(root,'node_modules/remotion')),voiceProfile:existsSync(path.resolve(root,profile)),voicePython:existsSync(python)};
console.log(JSON.stringify(report,null,2));
if(local.mode==='audio')console.log('Audio-only environment: import/registration ready; local cloned synthesis and ASR are not installed.');
else if(report.voicePython&&report.voiceProfile){const check=spawnSync(python,[path.join(root,'tools/voice/render.py'),'--profile',path.resolve(root,profile),'--check'],{cwd:root,stdio:'inherit'});if(check.status!==0)process.exit(check.status??1);}
else if(!report.voiceProfile)console.log('No voice registered yet. This is normal on first setup. Follow docs/VOICE.md. StarterDemo works now.');
else console.log('Preview/render ready; local voice runtime is not installed. See docs/SETUP.md.');
if(!report.remotion)process.exit(1);
