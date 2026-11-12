import fs from 'node:fs';
import path from 'node:path';
const slug=process.argv[2],title=process.argv.slice(3).join(' ');
if(!slug||!/^[a-z][a-z0-9-]{1,60}$/.test(slug)||!title)throw new Error('Usage: npm run new-video -- my-topic "My topic"');
const dir=path.resolve('projects',slug);
fs.mkdirSync(dir); // Fails if this project already exists.
const write=(name,v)=>fs.writeFileSync(path.join(dir,name),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n',{flag:'wx'});
write('project.json',{title,compositionId:slug.split('-').map(v=>v[0].toUpperCase()+v.slice(1)).join(''),author:'',credits:'',leadFrames:45,tailFrames:90});
write('outline.txt','Draft the outline from the supplied material, then obtain academic review.\n');
write('sources.txt','Record source filenames, pages, claim mappings, rights and facts needing future review.\n');
write('script.json',[]);write('visuals.json',{});
console.log(dir);
