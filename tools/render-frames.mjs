// Representative frame QA without driving the Studio UI.
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {selectComposition,renderStill,openBrowser} from '@remotion/renderer';
const slug=process.argv[2]||'starter-demo';
if(!/^[a-z0-9-]+$/.test(slug))throw new Error('Use a simple project slug.');
const data=JSON.parse(fs.readFileSync(`src/data/${slug}.json`,'utf8'));
const folder=path.resolve('.work/frames-'+Date.now());fs.mkdirSync(folder,{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),outDir:path.join(folder,'bundle')});
const browser=await openBrowser('chrome');
try{
 const composition=await selectComposition({serveUrl,id:data.compositionId,puppeteerInstance:browser});
 for(const s of data.scenes){const frame=s.from+Math.min(240,Math.floor(s.durationInFrames/2));await renderStill({serveUrl,composition,frame,output:path.join(folder,s.id+'.png'),scale:.5,puppeteerInstance:browser});console.log(s.id);}
 console.log(folder);
}finally{await browser.close({silent:true});}
