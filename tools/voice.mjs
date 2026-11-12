import {existsSync,readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const local=path.join(root,'.runtime/local.json');
const config=existsSync(local)?JSON.parse(readFileSync(local,'utf8')):{};
if(config.mode==='audio'){console.error('This is an audio-only environment for imported narration. Local TTS/ASR is not installed. See docs/SETUP.md.');process.exit(1);}
const python=config.python||path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
if(!existsSync(python)){console.error('Voice runtime is not installed. Ask Codex to follow docs/SETUP.md.');process.exit(1);}
const result=spawnSync(python,[path.join(root,'tools/voice/render.py'),...process.argv.slice(2)],{stdio:'inherit',cwd:root});
if(result.error)throw result.error;
process.exit(result.status??1);
