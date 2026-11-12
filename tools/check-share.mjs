// Inspect staged/tracked paths, not ignored personal folders.
import {spawnSync} from 'node:child_process';
const list=spawnSync('git',['ls-files','--cached','-z'],{encoding:'utf8'});
if(list.status!==0)throw new Error('Run from a Git checkout with files staged.');
const files=[...new Set(list.stdout.split('\0').filter(Boolean))];
const failures=[];
const approvedData=new Set(['src/data/starter-demo.json','src/data/registry.ts']);
for(const file of files){
 const privatePath=/^(?:\.runtime|\.venv(?:-audio)?|\.work|voiceover|renders)\//.test(file)
  ||(/^voices\//.test(file)&&file!=='voices/README.txt')
  ||(/^notes\//.test(file)&&file!=='notes/README.txt')
  ||(/^projects\//.test(file)&&!file.startsWith('projects/starter-demo/'))
  ||(/^public\//.test(file)&&!/^public\/(?:fonts|sfx)\//.test(file))
  ||(/^src\/data\//.test(file)&&!approvedData.has(file))
  ||/(^|\/)\.env($|\.)/.test(file);
 if(privatePath)failures.push(`Private/working path staged: ${file}`);
 if(/\.(?:mp4|mp3|wav|flac|m4a|ogg|zip|pt|safetensors)$/i.test(file)&&file!=='public/sfx/soft-swoosh.wav')failures.push(`Unexpected binary/media staged: ${file}`);
 if(/\.(?:md|txt|json|mjs|py|tsx?|html|sh|ps1|ya?ml)$/.test(file)){
  const item=spawnSync('git',['show',':'+file],{encoding:'utf8',maxBuffer:8*1024*1024});
  if(item.status!==0)throw new Error(`Cannot read staged ${file}`);
  if(/(?:[A-Z]:[\\/]Users[\\/]|\/Users\/[^/]+\/|\/home\/[^/]+\/)/.test(item.stdout))failures.push(`Machine-specific path staged: ${file}`);
  if(file==='src/data/registry.ts'&&/from\s+['"]\.\/(?!starter-demo\.json)/.test(item.stdout))failures.push('Registry imports a personal/ignored project. Share only the neutral registry.');
 }
}
if(failures.length){console.error(failures.join('\n'));process.exit(1);}
console.log(`Checked ${files.length} staged/tracked files: no private-path or personal-media matches. Review content before pushing.`);
