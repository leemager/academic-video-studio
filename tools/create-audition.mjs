import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const args=process.argv.slice(2);
const specPath=args.length===1?args[0]:args[1];
if(!specPath)throw new Error('Usage: node tools/create-audition.mjs spec.json (spec includes slug), or unique-slug spec.json');
const spec=JSON.parse(fs.readFileSync(specPath,'utf8'));
const slug=args.length===1?spec.slug:args[0];
if(!slug||!/^[a-z0-9-]+$/.test(slug))throw new Error('A unique lowercase slug is required.');
if(!spec.title||!spec.text||!spec.passageId||!Array.isArray(spec.takes)||spec.takes.length<1)throw new Error('Missing title, text, passageId or takes.');
for(const take of spec.takes){if(!take.file||!take.file.toLowerCase().endsWith('.wav')||!fs.existsSync(take.file))throw new Error('Each candidate must be an existing complete WAV passage.');}
fs.mkdirSync(path.resolve('public/auditions'),{recursive:true});
const dir=path.resolve('public/auditions',slug);fs.mkdirSync(dir,{recursive:false});
const manifest={title:spec.title,text:spec.text,passageId:spec.passageId,takes:[]};
for(const [i,t] of spec.takes.entries()){
 const bytes=fs.readFileSync(t.file),sha256=crypto.createHash('sha256').update(bytes).digest('hex');
 const file=`take-${String.fromCharCode(65+i)}-${sha256.slice(0,16)}.wav`;
 fs.writeFileSync(path.join(dir,file),bytes,{flag:'wx'});
 manifest.takes.push({id:String.fromCharCode(65+i),label:t.label||`Take ${String.fromCharCode(65+i)}`,note:t.note||'',file,sha256});
}
fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});
console.log(`npm run auditions -- ${slug}`);
