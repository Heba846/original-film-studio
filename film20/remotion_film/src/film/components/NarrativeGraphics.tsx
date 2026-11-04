/**
 * Authored, NON-PHOTOREAL narrative graphics. Each is built only from facts the narration states at that
 * moment (times, places, names, numbers it speaks). They are not documents and imitate no legal record.
 * Text is kept to the words being spoken; shapes and light carry the rest.
 */
import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {C, F, H, W, rand} from '../theme';
import {Dust, Rain} from './Atmosphere';
import {Base, clamp, ease, EhrChart, wrap} from './Evidence';

const night = 'radial-gradient(ellipse at 50% 45%, #1a2226, #070909 72%)';
const label = (s: React.CSSProperties = {}): React.CSSProperties => ({position: 'absolute', fontFamily: F.type, color: '#f3ead6', fontSize: 20, letterSpacing: 2, ...s});
const fadeIn = (f: number, a: number, d = 10) => interpolate(f, [a, a + d], [0, 1], clamp);

/* ------------------------------------------------------------------ Garage map (n024, n029, n032, n103) */
/** Top-down level 2 drawn as orange light on dark concrete: geography from script facts only. */
export const GarageMap: React.FC<Base> = ({dur, memory, beat = 'arrive'}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, dur], [0, 1], {...clamp, easing: ease});
  const sedanGone = beat === 'aftermath' ? interpolate(f, [dur * 0.35, dur * 0.65], [1, 0], clamp) : beat === 'call' ? 1 : 1;
  const time = {arrive: '4:08', call: '4:16', aftermath: '4:31', heard: '4:10', stairs: '4:10', listening: '4:10'}[beat] ?? '';
  const stall = (x: number, y: number, k: number) => <rect key={k} x={x} y={y} width={90} height={150} fill="none" stroke="#e89a3c" strokeOpacity={0.35} strokeWidth={2} />;
  const z = 1 + 0.06 * p + (beat === 'stairs' ? 0.25 : 0);
  return wrap(memory,
    <AbsoluteFill style={{background: night}}>
      <AbsoluteFill style={{transform: `scale(${z}) rotateX(${28 - 6 * p}deg)`, transformOrigin: beat === 'stairs' ? '78% 30%' : '50% 50%', perspective: 1200}}>
        <svg width={W} height={H}>
          {Array.from({length: 8}, (_, i) => stall(180 + i * 110, 120, i))}
          {Array.from({length: 8}, (_, i) => stall(180 + i * 110, 450, i + 8))}
          {Array.from({length: 6}, (_, i) => <circle key={i} cx={240 + i * 170} cy={360} r={70} fill="#e89a3c" opacity={0.05 + 0.02 * rand(i + Math.floor(f / 6))} />)}
          {/* Ivy's car, spot 2-14 */}
          <rect x={300} y={470} width={70} height={110} rx={10} fill="#22344a" stroke="#9cc2e8" strokeWidth={2} />
          {/* the silver sedan */}
          <rect x={850} y={140} width={74} height={120} rx={10} fill="#aab2b8" opacity={sedanGone} />
          {/* stairwell door */}
          <rect x={1080} y={110} width={60} height={70} fill="#2a2f33" stroke="#e8e0cc" strokeWidth={2} />
          {beat === 'stairs' && <>
            <path d="M1090 100 l12 -14 l12 0 l12 -14 l12 0" stroke="#e8e0cc" strokeWidth={2} fill="none" opacity={fadeIn(f, 8)} />
            <circle cx={1122} cy={72} r={9} fill="#e8d8b0" opacity={fadeIn(f, 16)} />
          </>}
          {beat === 'listening' && <>
            <rect x={1072} y={102} width={76} height={86} fill="none" stroke="#f3ead6" strokeWidth={3} opacity={0.5 + 0.4 * Math.abs(Math.sin(f / 10))} />
            <path d="M1090 100 l12 -14 l12 0 l12 -14 l12 0" stroke="#e8e0cc" strokeWidth={2} fill="none" opacity={0.6} />
            <ellipse cx={1122} cy={70} rx={10} ry={14} fill="#e8e0cc" opacity={0.18 * fadeIn(f, 10)} />
            <path d="M335 470 C 600 330, 900 200, 1072 150" stroke="#f3ead6" strokeWidth={2} strokeDasharray="6 8" fill="none" opacity={fadeIn(f, 16) * 0.6} />
          </>}
          {(beat === 'heard') && <>
            {[0, 1].map((k) => <circle key={k} cx={890} cy={200} r={40 + ((f * 4 + k * 60) % 220)} fill="none" stroke="#f3ead6"
              strokeOpacity={0.5 * (1 - ((f * 4 + k * 60) % 220) / 220)} strokeWidth={2} />)}
          </>}
        </svg>
      </AbsoluteFill>
      <div style={label({left: 64, top: 600, fontSize: 18, opacity: 0.85})}>LEVEL 2</div>
      <div style={label({left: 318 * 1, top: 640, fontSize: 18, opacity: beat === 'arrive' ? fadeIn(f, 6) : 0.6})}>2-14</div>
      <div style={label({right: 70, top: 600, fontSize: 30, opacity: fadeIn(f, 4)})}>{time}</div>
      {beat === 'heard' && <>
        <div style={label({left: 640, top: 70, opacity: fadeIn(f, 6)})}>HEARD · two shots</div>
        <div style={label({left: 640, top: 104, opacity: fadeIn(f, dur * 0.45)})}>SAW · what came after</div>
      </>}
      {beat === 'stairs' && <div style={label({right: 70, top: 70, opacity: fadeIn(f, 20)})}>half a flight up</div>}
      {beat === 'listening' && <div style={label({right: 70, top: 70, opacity: fadeIn(f, 20)})}>my only way out</div>}
      <Dust count={16} opacity={0.25} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ Ivy's reasoning (n031) */
/** Not a file: the chain of facts Ivy is given, drawn as nodes of light. */
export const CaseWeb: React.FC<Base> = ({dur, memory, beat = 'frankie'}) => {
  const f = useCurrentFrame();
  const k = ['frankie', 'ties', 'witness'].indexOf(beat);
  const node = (x: number, y: number, t: string, a: number, big = false) => (
    <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', opacity: a < 0 ? 0.55 : fadeIn(f, a, 12),
      fontFamily: big ? F.serif : F.type, fontSize: big ? 46 : 22, color: '#f3ead6', textAlign: 'center', whiteSpace: 'pre',
      textShadow: '0 0 24px rgba(232,154,60,.45)'}}>{t}</div>
  );
  const line = (d: string, a: number) => <path d={d} stroke="#e89a3c" strokeWidth={2} fill="none" pathLength={1} strokeDasharray={1}
    strokeDashoffset={a < 0 ? 0 : 1 - interpolate(f, [a, a + 18], [0, 1], clamp)} opacity={0.8} />;
  const water = Array.from({length: 12}, (_, i) => <path key={i} d={`M${120 + i * 90} ${600 + 6 * Math.sin(f / 10 + i)} q 20 -8 40 0 t 40 0`} stroke="#3b5a66" strokeWidth={2} fill="none" />);
  return wrap(memory,
    <AbsoluteFill style={{background: night}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {k === 0 && water}
        {k >= 1 && <>{line('M640 300 C 520 330, 420 380, 360 430', k === 1 ? 6 : -1)}{line('M640 300 C 760 330, 860 380, 920 430', k === 1 ? dur * 0.4 : -1)}</>}
        {k >= 2 && <>{line('M360 470 C 460 560, 820 560, 920 470', 4)}</>}
      </svg>
      {node(640, 250, 'Frankie Lombardi', k === 0 ? 6 : -1, true)}
      {k === 0 && node(640, 330, 'Gowanus Canal · two gunshot wounds', dur * 0.45)}
      {k >= 1 && node(340, 460, 'the Vescari family', k === 1 ? 12 : -1)}
      {k >= 1 && node(940, 460, 'quietly, the FBI', k === 1 ? dur * 0.5 : -1)}
      {k >= 2 && node(640, 590, 'a federal case', 8)}
      {k >= 2 && node(640, 650, 'and me, its witness', dur * 0.5)}
      <Dust count={20} opacity={0.3} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ Theo's debt (n037) */
export const DebtBeat: React.FC<Base> = ({dur, memory}) => {
  const f = useCurrentFrame();
  const grow = interpolate(f, [dur * 0.45, dur], [0, 1], clamp);
  return wrap(memory,
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, #1c1416, #070606 70%)'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center', fontFamily: F.serif, fontSize: 120, color: '#d9534a',
        opacity: fadeIn(f, 2, 12), transform: `scale(${1 + 0.06 * grow})`}}>$40,000</div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 420, textAlign: 'center', fontFamily: F.type, fontSize: 22, color: '#d9c9b8', letterSpacing: 3, opacity: fadeIn(f, dur * 0.25)}}>
        a betting app · then interest</div>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <path d={`M300 560 ${Array.from({length: 30}, (_, i) => `L${300 + i * 23} ${560 - Math.pow(i / 29, 2.2) * 160 * grow}`).join(' ')}`}
          stroke="#d9534a" strokeWidth={3} fill="none" opacity={0.7} />
      </svg>
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ "About ten seconds" (n051) */
export const Countdown: React.FC<Base> = ({dur, memory}) => {
  const f = useCurrentFrame();
  const n = Math.max(5, 10 - Math.floor(interpolate(f, [8, dur * 0.82], [0, 5.999], clamp)));
  const tunnel = interpolate(f, [0, dur * 0.82], [0.15, 0.85], clamp);
  const snap = f > dur * 0.82 ? interpolate(f, [dur * 0.82, dur * 0.82 + 4, dur], [0, 1, 0.15], clamp) : 0;
  const beat = Math.abs(Math.sin(f / 5));
  return wrap(memory,
    <AbsoluteFill style={{background: '#050505'}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 50%, rgba(170,40,30,${0.25 + 0.15 * beat}) 0%, rgba(0,0,0,1) ${70 - tunnel * 55}%)`}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 270, textAlign: 'center', fontFamily: F.serif, fontSize: 150, color: '#f3ead6',
        opacity: 0.85 - snap * 0.5, filter: `blur(${tunnel * 2.5}px)`}}>{n}</div>
      <AbsoluteFill style={{background: '#fff', opacity: snap * 0.8}} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ U01: Theo's arrest and the trade (n109) */
export const ArrestTransition: React.FC<Base> = ({dur, memory, beat = 'lights'}) => {
  const f = useCurrentFrame();
  if (beat === 'lights') {
    const ph = Math.floor(f / 7) % 2;
    return wrap(memory,
      <AbsoluteFill style={{background: '#060708'}}>
        <AbsoluteFill style={{background: `radial-gradient(ellipse at ${ph ? 30 : 70}% 40%, ${ph ? 'rgba(200,30,40,.45)' : 'rgba(40,80,220,.45)'}, transparent 60%)`}} />
        <div style={{position: 'absolute', left: 470, top: 250, width: 340, height: 220, background: 'rgba(235,235,225,.12)', border: '2px solid rgba(235,235,225,.45)',
          borderRadius: 6, transform: `rotate(-4deg) scale(${0.96 + 0.04 * fadeIn(f, 0, 20)})`, opacity: fadeIn(f, 6)}}>
          <div style={{position: 'absolute', right: -60, top: 30, width: 120, height: 46, background: '#e9e2c9', transform: 'rotate(12deg)',
            fontFamily: F.type, fontSize: 18, color: '#222', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>400</div>
        </div>
        <div style={label({left: 0, right: 0, top: 520, textAlign: 'center', opacity: fadeIn(f, dur * 0.4)})}>taped under the driver's seat</div>
      </AbsoluteFill>,
    );
  }
  if (beat === 'trade') {
    const tilt = interpolate(f, [0, dur * 0.6], [0, -9], {...clamp, easing: ease});
    return wrap(memory,
      <AbsoluteFill style={{background: night}}>
        <div style={{position: 'absolute', left: 240, top: 330, width: 800, height: 4, background: '#e8e0cc', transform: `rotate(${tilt}deg)`, opacity: 0.8}} />
        <div style={{position: 'absolute', left: 632, top: 334, width: 16, height: 120, background: '#e8e0cc', opacity: 0.5}} />
        <div style={label({left: 120, top: 380 + tilt * 6, width: 480, textAlign: 'center', fontSize: 22, opacity: fadeIn(f, 6), whiteSpace: 'nowrap'})}>my testimony against Nico</div>
        <div style={label({left: 760, top: 250 - tilt * 6, width: 300, textAlign: 'center', fontSize: 22, opacity: fadeIn(f, 16)})}>Theo walks</div>
        <Dust count={18} opacity={0.3} />
      </AbsoluteFill>,
    );
  }
  // car: night window, rain on the glass, streetlights passing; Nico's voice is never "shown"
  return wrap(memory,
    <AbsoluteFill style={{background: 'linear-gradient(180deg,#0b0f14,#141a20)'}}>
      {Array.from({length: 7}, (_, i) => {
        const x = ((i * 260 - f * 6) % 1600 + 1600) % 1600 - 160;
        return <div key={i} style={{position: 'absolute', left: x, top: 180 + 40 * rand(i), width: 180, height: 180, borderRadius: 90,
          background: 'radial-gradient(circle, rgba(232,154,60,.55), transparent 65%)', filter: 'blur(8px)'}} />;
      })}
      <Rain density={120} opacity={0.4} />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,.85) 0 9%, transparent 9% 91%, rgba(0,0,0,.85) 91%)'}} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ "Four minutes twenty seconds" (n142) */
export const ResusTimer: React.FC<Base> = ({dur, memory}) => {
  const f = useCurrentFrame();
  const secs = Math.round(interpolate(f, [4, dur - 8], [0, 260], clamp));
  const squeeze = Math.abs(Math.sin((f / 24) * Math.PI * 0.5));
  return wrap(memory,
    <AbsoluteFill style={{background: night}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 230, textAlign: 'center', fontFamily: F.type, fontSize: 110, color: '#f3ead6'}}>
        {Math.floor(secs / 60)}:{String(secs % 60).padStart(2, '0')}</div>
      <div style={{position: 'absolute', left: 590, top: 420, width: 100, height: 60, borderRadius: 30, border: '3px solid #9cc2e8',
        transform: `scaleX(${1 - 0.35 * squeeze})`, opacity: 0.7}} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ Why no indictment (n151) */
export const EvidenceRecap: React.FC<Base> = ({dur, memory}) => {
  const f = useCurrentFrame();
  const items = ["Enzo's statement", 'my testimony', "Frankie's gun", 'the chart'];
  const per = (dur * 0.7) / items.length;
  return wrap(memory,
    <AbsoluteFill style={{background: night}}>
      <div style={label({left: 0, right: 0, top: 120, textAlign: 'center', fontSize: 24, opacity: fadeIn(f, 2)})}>no indictment</div>
      {items.map((t, i) => (
        <div key={t} style={{position: 'absolute', left: 140 + i * 260, top: 320, width: 220, textAlign: 'center', fontFamily: F.serif,
          fontSize: 32, color: '#f3ead6', opacity: fadeIn(f, 8 + i * per), transform: `translateY(${(1 - fadeIn(f, 8 + i * per)) * 14}px)`}}>
          <div style={{height: 2, background: '#e89a3c', marginBottom: 18, opacity: 0.7}} />{t}</div>
      ))}
      <Dust count={16} opacity={0.3} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ April (n159) */
export const AprilEpilogue: React.FC<Base> = ({dur, memory, beat = 'june'}) => {
  const f = useCurrentFrame();
  if (beat === 'sal_letters') {
    const burn = interpolate(f, [dur * 0.3, dur], [0, 1], clamp);
    return wrap(memory,
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 70%, #3a2414, #0a0705 70%)'}}>
        {[0, 1, 2].map((i) => (
          <div key={i} style={{position: 'absolute', left: 420 + i * 60, top: 250 + i * 30, width: 360, height: 220, background: C.cream, transform: `rotate(${-8 + i * 7}deg)`,
            boxShadow: '0 20px 40px rgba(0,0,0,.5)', clipPath: i === 2 ? `inset(${burn * 100}% 0 0 0)` : undefined}}>
            <div style={{position: 'absolute', right: 20, top: 16, width: 90, height: 60, border: '2px solid #8a7a5a', borderRadius: 40, fontFamily: F.type,
              fontSize: 14, color: '#6a5a3a', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>Cefalù</div>
          </div>
        ))}
        <AbsoluteFill style={{background: `radial-gradient(ellipse at 60% 75%, rgba(255,140,40,${0.45 * burn}), transparent 45%)`}} />
      </AbsoluteFill>,
    );
  }
  if (beat === 'theo') {
    return wrap(memory,
      <AbsoluteFill style={{background: 'linear-gradient(180deg,#0b0e14 0 55%,#151a20 55%)'}}>
        {/* upstairs: Theo's lit window over the laundromat */}
        <div style={{position: 'absolute', left: 540, top: 90, width: 200, height: 150, background: 'linear-gradient(180deg,#f6d792,#e3a55a)',
          boxShadow: '0 0 90px rgba(246,215,146,.45)', opacity: 0.9}} />
        <div style={{position: 'absolute', left: 636, top: 90, width: 8, height: 150, background: '#2a2018'}} />
        {/* street level: the laundromat, front-loaders turning */}
        <div style={{position: 'absolute', left: 200, top: 330, width: 880, height: 300, background: 'linear-gradient(180deg,#cfe3ea,#8fb1bf)', opacity: 0.35}} />
        {[0, 1, 2, 3, 4].map((i) => (
          <div key={i} style={{position: 'absolute', left: 250 + i * 165, top: 420, width: 140, height: 160, background: '#dfe6e8', borderRadius: 8, opacity: 0.85}}>
            <div style={{position: 'absolute', left: 25, top: 40, width: 90, height: 90, borderRadius: 45, border: '6px solid #9aa7ad',
              background: `conic-gradient(from ${f * (4 + i)}deg, #7fa3b8, #c9d9e0, #7fa3b8)`}} />
          </div>
        ))}
      </AbsoluteFill>,
    );
  }
  // june: residency ends — a spring light and the one word she says
  return wrap(memory,
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 40% 30%, #f6e7c4, #c9b48a 70%)'}}>
      {Array.from({length: 16}, (_, i) => <div key={i} style={{position: 'absolute', left: 80 + rand(i) * 1100, top: 60 + rand(i + 9) * 560, width: 40, height: 22,
        borderRadius: '50%', background: '#7a9a4a', opacity: 0.55, transform: `rotate(${rand(i + 4) * 180 + f * 0.3}deg)`}} />)}
      <div style={{position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', fontFamily: F.serif, fontStyle: 'italic', fontSize: 64,
        color: '#3a2e1e', opacity: fadeIn(f, dur * 0.3, 16)}}>June</div>
    </AbsoluteFill>,
  );
};

export {EhrChart};
