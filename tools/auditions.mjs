import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const slug=process.argv[2]||'welcome',port=Number(process.env.AUDITION_PORT||3021);
if(!/^[a-z0-9-]+$/.test(slug))throw new Error('Invalid audition slug.');
const dir=path.join(root,'public/auditions',slug),manifest=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
const allowed=new Map();
for(const take of manifest.takes){
 if(path.basename(take.file)!==take.file)throw new Error('Audition files must be direct children.');
 const actual=fs.realpathSync(path.join(dir,take.file));
 if(path.dirname(actual)!==fs.realpathSync(dir))throw new Error('Symlink outside audition directory.');
 const hash=crypto.createHash('sha256').update(fs.readFileSync(actual)).digest('hex');
 if(hash!==take.sha256)throw new Error(`Changed audio: ${take.id}`);
 allowed.set('/audio/'+take.file,actual);
}
const token=crypto.randomBytes(24).toString('hex');
const html=fs.readFileSync(path.join(root,'tools/audition.html'),'utf8').replace('__TOKEN__',token);
const server=http.createServer(async(req,res)=>{
 const host=req.headers.host;
 if(![`localhost:${port}`,`127.0.0.1:${port}`].includes(host)){res.writeHead(403).end();return;}
 res.setHeader('X-Content-Type-Options','nosniff');
 res.setHeader('Cache-Control','no-store');
 res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; media-src 'self'; connect-src 'self'; frame-ancestors 'none'");
 const pathname=new URL(req.url,'http://localhost').pathname;
 if(req.method==='GET'&&pathname==='/'){res.setHeader('Content-Type','text/html; charset=utf-8');res.end(html);return;}
 if(req.method==='GET'&&pathname==='/manifest'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify(manifest));return;}
 if(req.method==='GET'&&allowed.has(pathname)){
  const file=allowed.get(pathname),size=fs.statSync(file).size,range=req.headers.range;
  res.setHeader('Content-Type','audio/wav');res.setHeader('Accept-Ranges','bytes');
  if(range){const m=/^bytes=(\d+)-(\d*)$/.exec(range);if(!m){res.writeHead(416).end();return;}const start=Number(m[1]),end=m[2]?Math.min(Number(m[2]),size-1):size-1;if(start>end||start>=size){res.writeHead(416,{'Content-Range':`bytes */${size}`}).end();return;}res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});fs.createReadStream(file,{start,end}).pipe(res);}
  else{res.setHeader('Content-Length',size);fs.createReadStream(file).pipe(res);}return;
 }
 if(req.method==='POST'&&pathname==='/choose'){
  if(req.headers['x-audition-token']!==token||req.headers.origin!==`http://${host}`){res.writeHead(403).end();return;}
  let body='';for await(const chunk of req){body+=chunk;if(body.length>1024){res.writeHead(413).end();return;}}
  let choice;try{choice=JSON.parse(body);}catch{res.writeHead(400).end();return;}
  const take=manifest.takes.find(t=>t.id===choice.id);if(!take){res.writeHead(400).end();return;}
  const stamp=new Date().toISOString().replace(/[:.]/g,'-'),folder=path.join(root,'voiceover/selections');fs.mkdirSync(folder,{recursive:true});
  const selection={audition:slug,passageId:manifest.passageId,text:manifest.text,take:take.id,file:`public/auditions/${slug}/${take.file}`,sha256:take.sha256,selectedAt:new Date().toISOString(),status:'selected by user in audition UI'};
  const filename=`${slug}-${stamp}-${crypto.randomBytes(3).toString('hex')}.json`;
  fs.writeFileSync(path.join(folder,filename),JSON.stringify(selection,null,2)+'\n',{flag:'wx'});
  res.setHeader('Content-Type','application/json');res.end(JSON.stringify({saved:`voiceover/selections/${filename}`,take:take.id}));return;
 }
 res.writeHead(404).end('Not found');
});
server.listen(port,'127.0.0.1',()=>console.log(`Auditions: http://localhost:${port}/ — ${slug}`));
