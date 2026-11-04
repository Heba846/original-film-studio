import React from 'react';
import {registerRoot, Composition, AbsoluteFill, Sequence, Video, Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from '../timeline.json';
import {FilmCompositions} from './film/FilmCompositions';

const FPS = 24;
const frames = (s: number) => Math.round(s * FPS);
const Captions = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const cue = timeline.captions.find(c => t >= c.start && t < c.end);
  if (!cue) return null;
  return <div style={{position:'absolute', bottom:52, width:'100%', textAlign:'center', padding:'0 80px',boxSizing:'border-box'}}>
    <span style={{fontFamily:'Arial',fontSize:32,lineHeight:1.4,color:'white',background:'rgba(0,0,0,.76)',padding:'7px 14px',boxDecorationBreak:'clone',whiteSpace:'pre-line'}}>{cue.text}</span>
  </div>;
};
const Opening = () => <AbsoluteFill style={{backgroundColor:'black'}}>
  {timeline.shots.map((s,i) => <Sequence key={i} from={frames(s.start)} durationInFrames={frames(s.end)-frames(s.start)}>
    <AbsoluteFill style={{overflow:'hidden'}}><Video src={staticFile(s.file)} startFrom={frames(s.sourceStart)} muted style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${s.scale})`,transformOrigin:s.origin}} /></AbsoluteFill>
  </Sequence>)}
  {timeline.audio.map(a => <Sequence key={a.file} from={frames(a.start)} durationInFrames={Math.ceil((a.end-a.start)*FPS)}><Audio src={staticFile(a.file)} /></Sequence>)}
  <Captions />
</AbsoluteFill>;
registerRoot(() => <>
  <Composition id="Opening" component={Opening} durationInFrames={384} fps={FPS} width={1280} height={720} />
  <FilmCompositions />
</>);
