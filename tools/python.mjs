// Run a helper using this project's configured voice Python.
import {existsSync,readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const file=path.join(root,'.runtime/local.json');
const config=existsSync(file)?JSON.parse(readFileSync(file,'utf8')):{};
const python=config.python||path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
if(!existsSync(python)){console.error('Voice Python is missing. Follow docs/SETUP.md.');process.exit(1);}
const result=spawnSync(python,process.argv.slice(2),{cwd:root,stdio:'inherit'});
if(result.error)throw result.error;
process.exit(result.status??1);
