import React from 'react';
import {AbsoluteFill} from 'remotion';
import {F} from '../theme';

/** Editor-only slate for picture that does not exist yet. Deliberately loud so it can never be mistaken for
 *  finished footage. Shows exactly what the plan expects here. Film20-Final refuses to render while any exist. */
export const Placeholder: React.FC<{
  shotId: string; slug?: string; event: string; status: string; segment: string; speaker: string; text: string;
  plan?: string; reuse?: string; memory?: boolean; unresolved?: boolean;
}> = ({shotId, slug, event, status, segment, speaker, text, plan, reuse, memory, unresolved}) => (
  <AbsoluteFill style={{background: unresolved ? 'repeating-linear-gradient(135deg, #2a0d0d 0 26px, #3a1212 26px 52px)'
    : 'repeating-linear-gradient(135deg, #191919 0 26px, #222 26px 52px)', color: '#eee', fontFamily: F.ui, padding: 60, boxSizing: 'border-box', justifyContent: 'center'}}>
    <div style={{border: `3px dashed ${unresolved ? '#ff5a4a' : '#f2c200'}`, padding: '28px 36px', background: 'rgba(0,0,0,.74)'}}>
      <div style={{color: unresolved ? '#ff5a4a' : '#f2c200', fontSize: 18, letterSpacing: 3, fontWeight: 700}}>
        {unresolved ? 'UNRESOLVED — NO PICTURE PLANNED' : 'EDITOR-ONLY PLACEHOLDER · PLANNED, NOT DELIVERED'}
      </div>
      <div style={{fontSize: 36, fontWeight: 700, marginTop: 10}}>
        {shotId}{slug ? <span style={{fontWeight: 400, color: '#bbb'}}> · {slug}</span> : null}
        <span style={{fontSize: 20, color: '#ff8a65', fontWeight: 600}}> · {status.toUpperCase().replace(/_/g, ' ')}</span>
        {memory ? <span style={{fontSize: 20, color: '#9cc2e8'}}> · MEMORY</span> : null}
      </div>
      <div style={{fontSize: 25, marginTop: 8, lineHeight: 1.3}}>{event}</div>
      {plan && <div style={{fontSize: 17, marginTop: 10, color: '#9fd39f', fontFamily: 'JetBrains Mono, monospace'}}>{plan}</div>}
      {reuse && <div style={{fontSize: 16, marginTop: 6, color: '#9cc2e8'}}>reuse: {reuse}</div>}
      <div style={{fontSize: 16, marginTop: 16, color: '#aaa', lineHeight: 1.45}}>
        {segment} · {speaker.toUpperCase()} — {text.length > 150 ? text.slice(0, 147) + '…' : text}
      </div>
    </div>
  </AbsoluteFill>
);
