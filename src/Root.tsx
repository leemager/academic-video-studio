import {Composition} from 'remotion';
import {LectureVideo} from './Composition';
import {projects} from './data/registry';

export const RemotionRoot=()=> <>{projects.map(project=><Composition key={project.compositionId} id={project.compositionId} component={LectureVideo} durationInFrames={project.durationInFrames} fps={project.fps} width={project.width} height={project.height} defaultProps={{project}}/>)}</>;
