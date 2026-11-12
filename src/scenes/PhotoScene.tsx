import {useCurrentFrame,interpolate} from 'remotion';
import type {SceneData} from '../types';
import {C,Photo,Reveal,Rule,serif,ease} from '../design';
export const PhotoScene=({scene}:{scene:SceneData})=>{
 const f=useCurrentFrame(),beat=Math.min(scene.beats.length-1,Math.floor(Math.max(0,f-100)/(scene.durationInFrames/Math.max(1,scene.beats.length))));
 if(scene.kind==='portrait'||scene.kind==='quote')return <>
  <Photo image={scene.image!} duration={scene.durationInFrames} position="center 25%" style={{position:'absolute',left:0,top:0,width:800,height:1080}}/>
  <div style={{position:'absolute',left:800,width:1120,height:1080,background:C.paper,padding:'125px 100px',boxSizing:'border-box'}}>
   <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:scene.kind==='quote'?86:104,fontWeight:400,lineHeight:1.04,margin:0}}>{scene.kind==='quote'?'“'+scene.title+'”':scene.title}</h1></Reveal>
   <Reveal delay={20}><p style={{fontSize:30,color:C.muted,lineHeight:1.5,marginTop:38}}>{scene.detail}</p></Reveal>
   {scene.beats[beat]&&<div style={{position:'absolute',bottom:130,left:100,right:100,borderTop:`1px solid ${C.line}`,paddingTop:30,fontSize:40,lineHeight:1.25}}>{scene.beats[beat]}</div>}
  </div>
 </>;
 return <>
  <Photo image={scene.image!} duration={scene.durationInFrames} style={{position:'absolute',inset:0}}/>
  <div style={{position:'absolute',inset:0,background:'linear-gradient(90deg,rgba(15,18,20,.92),rgba(15,18,20,.45) 62%,rgba(15,18,20,.1))'}}/>
  <div style={{position:'absolute',left:130,top:180,width:1120,color:C.paper}}>
   <Reveal><div style={{width:90,height:6,background:'#e45c67',marginBottom:38}}/><h1 style={{fontFamily:serif,fontSize:scene.kind==='closing'?130:128,lineHeight:1.02,fontWeight:400,margin:0,whiteSpace:'pre-line'}}>{scene.title}</h1></Reveal>
   <Reveal delay={20}><p style={{fontSize:38,lineHeight:1.4,maxWidth:900,marginTop:35}}>{scene.detail}</p></Reveal>
  </div>
  {scene.kind!=='closing'&&scene.beats[beat]&&<div style={{position:'absolute',left:134,bottom:130,fontSize:42,color:C.paper,opacity:interpolate(f,[50,90],[0,1],ease)}}>{scene.beats[beat]}</div>}
 </>;
};
