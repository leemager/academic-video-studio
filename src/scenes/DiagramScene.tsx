import {interpolate,useCurrentFrame} from 'remotion';
import type {SceneData} from '../types';
import {C,Reveal,Rule,serif,ease} from '../design';
export const DiagramScene=({scene}:{scene:SceneData})=>{
 const f=useCurrentFrame();
 if(scene.kind==='network')return <div style={{padding:'110px 130px'}}>
  <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:100,fontWeight:400,margin:0}}>{scene.title}</h1><p style={{fontSize:32,color:C.muted}}>{scene.detail}</p></Reveal>
  <svg width="1660" height="500" style={{position:'absolute',left:130,top:435}}>
   <path d="M320 250 C500 50 720 50 830 250 S1180 450 1340 250" fill="none" stroke={C.red} strokeWidth="3" strokeDasharray="1400" strokeDashoffset={interpolate(f,[30,180],[1400,0],ease)}/>
   <path d="M320 250 C500 450 720 450 830 250 S1180 50 1340 250" fill="none" stroke={C.line} strokeWidth="2"/>
   {[320,830,1340].map((x,i)=><g key={x} opacity={interpolate(f,[30+i*20,55+i*20],[0,1],ease)}><circle cx={x} cy="250" r="116" fill={i===1?C.red:C.paper} stroke={C.red} strokeWidth="2"/><text x={x} y="258" textAnchor="middle" fill={i===1?C.paper:C.ink} fontFamily="Inter" fontSize={scene.beats[i].length>14?25:31}>{scene.beats[i]}</text></g>)}
  </svg>
 </div>;
 if(scene.kind==='growth')return <div style={{padding:'110px 130px'}}>
  <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:106,fontWeight:400,margin:0}}>{scene.title}</h1><p style={{fontSize:32,color:C.muted}}>{scene.detail}</p></Reveal>
  <div style={{display:'flex',gap:120,position:'absolute',left:160,bottom:150,right:160,alignItems:'flex-end',height:400}}>
   {scene.beats.filter(b=>/\d/.test(b)).map((b,i)=>{const [label,value]=b.split('|');return <div key={b} style={{flex:1}}><div style={{fontFamily:serif,fontSize:110,marginBottom:20}}>{value}</div><div style={{height:interpolate(f,[40+i*35,120+i*35],[0,parseFloat(value)*1.3],ease),background:i?C.ink:C.red}}/><div style={{fontSize:36,marginTop:28}}>{label}</div></div>;})}
  </div>
 </div>;
 return <div style={{padding:'110px 130px'}}>
  <Reveal><Rule/><h1 style={{fontFamily:serif,fontSize:110,fontWeight:400,margin:0}}>{scene.title}</h1><p style={{fontSize:34,color:C.muted}}>{scene.detail}</p></Reveal>
  <div style={{position:'absolute',left:130,right:130,top:460,height:350,display:'flex',gap:65}}>
   {scene.beats.map((b,i)=><Reveal key={b} delay={40+i*45} style={{flex:1,borderTop:`3px solid ${i===0?C.line:C.red}`,paddingTop:42}}><div style={{fontFamily:serif,fontSize:80,lineHeight:1.1}}>{b}</div></Reveal>)}
  </div>
 </div>;
};
