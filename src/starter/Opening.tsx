import {interpolate,useCurrentFrame} from 'remotion';
import {C,In,Wave,ease,type GuideScene} from './theme';
export const Opening=({scene}:{scene:GuideScene})=>{const f=useCurrentFrame();return <>
 <In style={{position:'absolute',left:125,top:160,fontSize:125,fontWeight:650,lineHeight:1.08,letterSpacing:-5}}>This is my<br/><span style={{color:C.mint}}>cloned voice.</span></In>
 <In delay={16} style={{position:'absolute',left:130,top:490,fontSize:42,color:C.muted}}>A guide to Academic video studio</In>
 <div style={{position:'absolute',left:130,top:690,opacity:interpolate(f,[5,30],[0,1],ease)}}><Wave values={scene.wave} width={1650} height={160} progress={f/scene.durationInFrames}/></div>
 </>};
