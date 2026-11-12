import {loadFont} from '@remotion/fonts';
import {CanvasImage, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {CSSProperties, ReactNode} from 'react';
export const C={paper:'#f1ebdf',ink:'#202324',red:'#176b70',muted:'#6b6862',line:'#cbc2b4'};
export const serif='Caslon, Georgia, serif';
export const sans='Inter, Arial, sans-serif';
export const ease={extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.bezier(.16,1,.3,1)} as const;
loadFont({family:'Caslon',url:staticFile('fonts/librecaslondisplay-LibreCaslonDisplay-Regular.ttf')});
loadFont({family:'Inter',url:staticFile('fonts/inter-Inter[opsz,wght].ttf'),weight:'100 900'});
export const Reveal=({children,delay=0,style={}}:{children:ReactNode;delay?:number;style?:CSSProperties})=>{
 const f=useCurrentFrame();return <div style={{opacity:interpolate(f,[delay,delay+24],[0,1],ease),translate:`0 ${interpolate(f,[delay,delay+30],[30,0],ease)}px`,...style}}>{children}</div>;
};
export const Photo=({image,duration=900,style={},position='center'}:{image:string;duration?:number;style?:CSSProperties;position?:string})=>{
 const f=useCurrentFrame();return <div style={{overflow:'hidden',...style}}><CanvasImage src={staticFile(image)} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:position,scale:interpolate(f,[0,duration],[1.025,1.10],{extrapolateRight:'clamp'})}}/></div>;
};
export const Rule=()=> <div style={{width:92,height:5,background:C.red,marginBottom:38}}/>;
export const Paper=({children,dark=false}:{children:ReactNode;dark?:boolean})=><div style={{position:'absolute',inset:0,background:dark?C.ink:C.paper,color:dark?C.paper:C.ink,fontFamily:sans}}>{children}</div>;
