import {AbsoluteFill,Sequence,useCurrentFrame,interpolate,staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import type {ProjectData,SceneData} from './types';
import {C,Paper,Reveal,serif} from './design';
import {PhotoScene} from './scenes/PhotoScene';
import {TextScene} from './scenes/TextScene';
import {DiagramScene} from './scenes/DiagramScene';
export const Scene=({scene}:{scene:SceneData})=><Paper>{['hero','photo','portrait','quote','closing'].includes(scene.kind)?<PhotoScene scene={scene}/>:['network','growth','contrast'].includes(scene.kind)?<DiagramScene scene={scene}/>:<TextScene scene={scene}/>}</Paper>;
const Wipe=()=>{const f=useCurrentFrame();return <AbsoluteFill style={{background:C.red,translate:`${interpolate(f,[0,14,28],[-100,0,100])}% 0`}}/>;};
const Intro=({project}:{project:ProjectData})=><Paper><div style={{position:'absolute',left:130,top:220,right:130}}><Reveal><div style={{fontFamily:serif,fontSize:135,lineHeight:1.05}}>{project.title}</div>{project.subtitle&&<p style={{fontSize:44,color:C.red}}>{project.subtitle}</p>}{project.author&&<p style={{fontSize:32,marginTop:70}}>{project.author}</p>}</Reveal></div></Paper>;
const Credits=({project}:{project:ProjectData})=><Paper dark><div style={{position:'absolute',inset:130,display:'flex',flexDirection:'column',justifyContent:'center'}}><Reveal><div style={{fontFamily:serif,fontSize:105}}>{project.title}</div>{project.credits&&<p style={{fontSize:36,lineHeight:1.7,whiteSpace:'pre-line',maxWidth:1500}}>{project.credits}</p>}</Reveal></div></Paper>;
export const LectureVideo=({project}:{project:ProjectData})=>{
 const last=project.scenes.at(-1);
 const end=last?last.from+last.durationInFrames:project.leadFrames;
 return <AbsoluteFill style={{background:C.paper}}>
  {project.leadFrames>0&&<Sequence durationInFrames={project.leadFrames} name="Opening"><Intro project={project}/></Sequence>}
  {project.scenes.map(scene=><Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames} name={scene.title}><Scene scene={scene}/></Sequence>)}
  {project.audio&&<Sequence from={project.audioFromFrames??project.leadFrames} name="Continuous narration"><Audio src={staticFile(project.audio)} /></Sequence>}
  {project.scenes.filter(s=>s.transition&&s.from>=14).map(scene=><Sequence key={'wipe'+scene.id} from={scene.from-14} durationInFrames={29} name="Transition"><Wipe/><Audio src={staticFile('sfx/soft-swoosh.wav')} volume={0.16}/></Sequence>)}
  {project.durationInFrames>end&&<Sequence from={end} durationInFrames={project.durationInFrames-end} name="Closing"><Credits project={project}/></Sequence>}
 </AbsoluteFill>;
};
