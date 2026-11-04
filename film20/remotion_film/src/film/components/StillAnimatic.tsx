import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {F} from '../theme';

/** Workbench-only: QA-approved still with a slow push, clearly badged as not yet animated. Never used in strict renders. */
export const StillAnimatic: React.FC<{src: string; dur: number; shotId: string; slug?: string}> = ({src, dur, shotId, slug}) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, Math.max(1, dur)], [1.0, 1.06], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${s})`}} />
      <div style={{position: 'absolute', right: 24, top: 24, padding: '6px 12px', background: 'rgba(0,0,0,.7)', color: '#f2c200',
        border: '2px dashed #f2c200', fontFamily: F.ui, fontSize: 16, letterSpacing: 2}}>
        APPROVED STILL · NOT ANIMATED · {shotId}{slug ? ` ${slug}` : ''}
      </div>
    </AbsoluteFill>
  );
};
