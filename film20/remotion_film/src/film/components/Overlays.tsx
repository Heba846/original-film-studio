import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {F} from '../theme';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Short date/time stamp, lower left, fades in/out. Only dates the script or canon states. */
export const DateStamp: React.FC<{text: string; dur: number}> = ({text, dur}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [4, 16, dur - 14, dur - 2], [0, 1, 1, 0], clamp);
  const ls = interpolate(f, [4, 30], [6, 3.5], clamp);
  return (
    <div style={{position: 'absolute', left: 64, top: 52, opacity: o, fontFamily: F.type, color: '#f3ead6',
      fontSize: 21, letterSpacing: ls, textShadow: '0 2px 10px rgba(0,0,0,.9)'}}>
      {text}
    </div>
  );
};

/** Chapter title: understated, upper right, never a full-screen card. */
export const ChapterTitle: React.FC<{title: string; dur: number}> = ({title, dur}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [6, 22, dur - 18, dur - 4], [0, 0.9, 0.9, 0], clamp);
  return (
    <div style={{position: 'absolute', right: 64, top: 50, opacity: o, fontFamily: F.serif, fontStyle: 'italic',
      color: '#f3ead6', fontSize: 30, textShadow: '0 2px 12px rgba(0,0,0,.9)'}}>
      {title}
    </div>
  );
};

export type Cue = {start: number; end: number; text: string; seg: string; estimated: boolean};

/** Burned-in captions for previews (the SRT sidecar is exported separately). */
export const Captions: React.FC<{cues: Cue[]; offsetS: number; fps: number}> = ({cues, offsetS, fps}) => {
  const t = useCurrentFrame() / fps + offsetS;
  const cue = cues.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 46}}>
      <div style={{fontFamily: F.ui, fontSize: 29, lineHeight: 1.35, color: cue.estimated ? '#ffd27a' : 'white', textAlign: 'center',
        whiteSpace: 'pre-line', background: 'rgba(0,0,0,.62)', padding: '6px 16px', borderRadius: 4, maxWidth: 1060}}>
        {cue.estimated ? '[PICKUP NOT RECORDED] ' : ''}{cue.text}
      </div>
    </AbsoluteFill>
  );
};

/** Workbench heads-up display (editor-only). */
export const Hud: React.FC<{
  seg?: {id: string; speaker: string; chapter: string; audio_status: string};
  block?: {shot: string; status: string; short_s: number};
  tS: number; totalS: number; estimate: boolean; label: string;
}> = ({seg, block, tS, totalS, estimate, label}) => {
  const mm = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, '0')}`;
  const col = (st?: string) => (st === 'approved' || st === 'code' || st === 'ok' ? '#7CFC9A' : st === 'restricted' ? '#ffd27a' : '#ff6b5b');
  return (
    <div style={{position: 'absolute', left: 10, bottom: 8, fontFamily: 'JetBrains Mono, monospace', fontSize: 13, color: '#ddd',
      background: 'rgba(0,0,0,.7)', padding: '4px 8px', borderRadius: 3, display: 'flex', gap: 14}}>
      <span style={{color: '#f2c200'}}>{label}</span>
      <span>{mm(tS)} / {mm(totalS)}{estimate ? ' EST' : ''}</span>
      {seg && <span>{seg.chapter} · {seg.id} · {seg.speaker.toUpperCase()}</span>}
      {seg && <span style={{color: col(seg.audio_status)}}>audio:{seg.audio_status}</span>}
      {block && <span style={{color: col(block.status)}}>visual:{block.shot}:{block.status}{block.short_s > 0 ? ` short ${block.short_s}s` : ''}</span>}
    </div>
  );
};
