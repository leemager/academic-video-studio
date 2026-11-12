import {useCurrentFrame,interpolate} from 'remotion';
import type {SceneData} from '../types';
import {C,Photo,Reveal,Rule,serif,ease} from '../design';
export const TextScene=({scene}:{scene:SceneData})=>{
 const f=useCurrentFrame();
 const step=Math.min(scene.beats.length-1,Math.floor(f/(scene.durationInFrames/Math.max(1,scene.beats.length))));
 const local=f-step*(scene.durationInFrames/Math.max(1,scene.beats.length));
 if(scene.kind==='timeline')return <>
  <Photo image={scene.image!} duration={scene.durationInFrames} style={{position:'absolute',right:0,top:0,width:700,height:1080}}/>
  <div style={{position:'absolute',left:0,top:0,width:1220,height:1080,background:C.paper,padding:'115px 125px',boxSizing:'border-box'}}>
   <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:100,fontWeight:400,margin:0}}>{scene.title}</h1></Reveal>
   <div style={{marginTop:65,borderLeft:`2px solid ${C.line}`,paddingLeft:50}}>{scene.beats.map((b,i)=><Reveal delay={40+i*100} key={b} style={{marginBottom:55}}><div style={{fontFamily:serif,fontSize:100,color:C.red,lineHeight:1}}>{b.split('|')[0]}</div><div style={{fontSize:36,marginTop:12}}>{b.split('|')[1]}</div></Reveal>)}</div>
  </div>
 </>;
 if(scene.kind==='book')return <>
  <div style={{position:'absolute',left:180,top:135,width:580,height:800,background:C.red,color:C.paper,boxShadow:'24px 25px 0 #c9c0b2',rotate:`${interpolate(f,[0,scene.durationInFrames],[-4,-1])}deg`,padding:65,boxSizing:'border-box'}}>
   <div style={{borderTop:'2px solid #d09194',paddingTop:40,fontFamily:serif,fontSize:75,lineHeight:1.05}}>{scene.title}</div><div style={{position:'absolute',bottom:85,fontSize:30,left:65,right:50}}>{scene.detail}</div>
  </div>
  <div style={{position:'absolute',left:940,right:130,top:290}}><Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:95,lineHeight:1.1,fontWeight:400,margin:0}}>{scene.beats[step]}</h1></Reveal></div>
 </>;
 if(scene.kind==='statement')return <div style={{position:'absolute',inset:0,background:C.red,color:C.paper,padding:'150px 145px',boxSizing:'border-box'}}>
  <Reveal><h1 style={{fontFamily:serif,fontSize:130,fontWeight:400,lineHeight:1.02,maxWidth:1500,margin:0}}>{scene.title}</h1><p style={{fontSize:38,marginTop:40,color:'#d7eeea'}}>{scene.detail}</p></Reveal>
  <div style={{position:'absolute',left:145,bottom:160,right:145,fontSize:48,borderTop:'1px solid #7db3ad',paddingTop:40}}>{scene.beats[step]}</div>
 </div>;
 const labels=(scene.kind==='names'?scene.beats:(scene.beats[step]||'').split('|'));
 return <div style={{padding:'110px 130px'}}>
  <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:105,fontWeight:400,lineHeight:1.05,margin:0,maxWidth:1550}}>{scene.title}</h1>{scene.detail&&<p style={{fontSize:32,color:C.muted,marginTop:30}}>{scene.detail}</p>}</Reveal>
  <div style={{position:'absolute',left:130,right:130,top:430,opacity:interpolate(local,[0,25],[.2,1],ease)}}>
   {labels.map((b,i)=><div key={b} style={{borderTop:`1px solid ${C.line}`,padding:'25px 0',fontFamily:serif,fontSize:labels.length>3?66:78,lineHeight:1.06,color:i===0?C.red:C.ink}}>{b}</div>)}
  </div>
 </div>;
};
