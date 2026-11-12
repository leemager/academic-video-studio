import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const [project,take]=process.argv.slice(2);
if(!project||!take)throw new Error('Usage: node tools/prepare-video.mjs my-topic voiceover/my-topic/take-01');
if(!/^[a-z0-9-]+$/.test(project)) throw new Error('Use a simple project slug.');
const dir=path.join(root,'projects',project);
const manifest=JSON.parse(fs.readFileSync(path.resolve(root,take,'manifest.json'),'utf8'));
const audio=fs.readFileSync(path.resolve(root,take,'narration.wav'));
const hash=crypto.createHash('sha256').update(audio).digest('hex');
if(hash!==manifest.narration_sha256) throw new Error('Narration was changed after QA.');
const file=`${project}/audio/narration-${hash.slice(0,16)}.wav`;
fs.mkdirSync(path.dirname(path.join(root,'public',file)),{recursive:true});
if(!fs.existsSync(path.join(root,'public',file))) fs.writeFileSync(path.join(root,'public',file),audio,{flag:'wx'});
else if(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'public',file))).digest('hex')!==hash) throw new Error('Existing public asset was changed. Preserve it and investigate before updating the edit.');
const config=JSON.parse(fs.readFileSync(path.join(dir,'project.json'),'utf8'));
const visuals=JSON.parse(fs.readFileSync(path.join(dir,'visuals.json'),'utf8'));
const kinds=new Set(['hero','photo','portrait','quote','closing','network','growth','contrast','timeline','book','statement','names','text']);
for(const scene of manifest.scenes){
 const visual=visuals[scene.id];
 if(!visual||!kinds.has(visual.kind)||!visual.title||!Array.isArray(visual.beats))throw new Error(`Missing/invalid visual for ${scene.id}`);
 if(['hero','photo','portrait','quote','closing','timeline'].includes(visual.kind)&&!visual.image)throw new Error(`Image required for ${scene.id}`);
 if(visual.kind==='network'&&visual.beats.length!==3)throw new Error('Network layout requires three beats.');
 if(['from','durationInFrames','id','text'].some(k=>k in visual))throw new Error('Visual data must not override narration timing or text.');
}
const fps=30,lead=config.leadFrames??45,tail=config.tailFrames??90;
if(!Number.isInteger(lead)||lead<0||!Number.isInteger(tail)||tail<0)throw new Error('Lead/tail must be nonnegative frame counts.');
const result={...config,fps,width:1920,height:1080,audio:file,audioHash:hash,leadFrames:lead,durationInFrames:lead+Math.ceil(manifest.duration_seconds*fps)+tail,
  scenes:manifest.scenes.map((s,i)=>({id:s.id,text:s.text,from:lead+Math.round(s.start_seconds*fps),durationInFrames:Math.max(1,(i+1<manifest.scenes.length?Math.round(manifest.scenes[i+1].start_seconds*fps):Math.ceil(manifest.duration_seconds*fps))-Math.round(s.start_seconds*fps)),...visuals[s.id]}))};
fs.mkdirSync(path.join(root,'src/data'),{recursive:true});
const target=path.join(root,'src/data',project+'.json');
// The compiled edit is versioned in Git; immutable audio remains separate.
const stamp=new Date().toISOString().replace(/[:.]/g,'-');
const history=path.join(dir,'edits');fs.mkdirSync(history,{recursive:true});
if(fs.existsSync(target))fs.copyFileSync(target,path.join(history,stamp+'-previous.json'),fs.constants.COPYFILE_EXCL);
fs.writeFileSync(target,JSON.stringify(result,null,2)+'\n');
const registry=path.join(root,'src/data/registry.ts');
const projects=fs.readdirSync(path.join(root,'src/data')).filter(f=>f.endsWith('.json')).map(f=>f.slice(0,-5));
fs.writeFileSync(registry,projects.map((p,i)=>`import project${i} from './${p}.json';`).join('\n')+'\nexport const projects = ['+projects.map((_,i)=>`project${i}`).join(', ')+'];\n');
const records=path.join(dir,'selections');fs.mkdirSync(records,{recursive:true});
fs.writeFileSync(path.join(records,stamp+'.json'),JSON.stringify({sourceTake:take,audio:file,sha256:hash,reference_sha256:manifest.reference_sha256,scenes:manifest.scenes.map(s=>({id:s.id,sha256:s.sha256})),status:'production draft; human review pending'},null,2),{flag:'wx'});
console.log(JSON.stringify({composition:result.compositionId,seconds:result.durationInFrames/fps,audio:file,sha256:hash},null,2));
