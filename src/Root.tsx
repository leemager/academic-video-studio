import {Composition} from 'remotion';
import {LectureVideo} from './Composition';
import {Guide} from './starter/Guide';
import {projects} from './data/registry';
import type {ProjectData} from './types';

const ProjectVideo=({project}:{project:ProjectData})=>project.compositionId==='StarterDemo'?<Guide/>:<LectureVideo project={project}/>;

export const RemotionRoot=()=> <>{projects.map(project=><Composition key={project.compositionId} id={project.compositionId} component={ProjectVideo} durationInFrames={project.durationInFrames} fps={project.fps} width={project.width} height={project.height} defaultProps={{project}}/>)}</>;
