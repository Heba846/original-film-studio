/**
 * Code-native evidence scenes, staged as short BEATS that follow the narration.
 * Every legible word comes from the script / canon ledger. Anything the text does not state is drawn as
 * ILLEGIBLE ink on purpose, so the film never invents a record, a clause or a fact through set dressing.
 * Only the first beat of a document "arrives"; later beats move the camera to the line being spoken.
 */
import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, F, H, W, rand} from '../theme';
import {Dust, Memory} from './Atmosphere';

export type Base = {dur: number; memory?: boolean; beat?: string};
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = Easing.bezier(0.33, 0, 0.2, 1);

/* ------------------------------------------------------------------ primitives */

/** Camera framing for a beat: where the lens looks (%), how close, and whether the object arrives. */
export type Frame = {fx: number; fy: number; zoom: number; enter?: boolean; tilt?: number};

/** Desk/lamp stage with two-layer parallax (background drifts at 40% of the object layer). */
export const DeskScene: React.FC<{dur: number; frame: Frame; children: React.ReactNode; surface?: string; lampX?: number}> = ({
  dur, frame, children, surface = '#2a1d14', lampX = 38,
}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(f, [0, dur], [0, 1], {...clamp, easing: ease});
  const rise = frame.enter ? spring({frame: f, fps, config: {damping: 200}, durationInFrames: 18}) : 1;
  const z = frame.zoom * (1 + 0.035 * p);
  const origin = `${frame.fx}% ${frame.fy}%`;
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at ${lampX}% 35%, rgba(255,214,150,.38), rgba(0,0,0,0) 55%), ${surface}`,
        transform: `scale(${1.04 + Math.max(0, z - 1) * 0.4})`, transformOrigin: origin,
      }}>
        <WoodGrain />
      </AbsoluteFill>
      <AbsoluteFill style={{perspective: 1400, transform: `translateY(${(1 - rise) * 30}px) scale(${z})`, transformOrigin: origin, opacity: rise}}>
        <AbsoluteFill style={{transform: `rotateX(${(frame.tilt ?? 8) * (1 - 0.3 * p)}deg)`, transformStyle: 'preserve-3d'}}>{children}</AbsoluteFill>
      </AbsoluteFill>
      <AbsoluteFill style={{background: `radial-gradient(ellipse at ${lampX}% 40%, rgba(0,0,0,0) 35%, rgba(0,0,0,.65) 100%)`}} />
      <Dust count={22} opacity={0.35} />
    </AbsoluteFill>
  );
};

const WoodGrain: React.FC = () => (
  <svg width={W} height={H} style={{position: 'absolute', opacity: 0.35, mixBlendMode: 'overlay'}}>
    <filter id="wood"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.09" numOctaves="3" seed="4" /><feColorMatrix type="saturate" values="0" /></filter>
    <rect width="100%" height="100%" filter="url(#wood)" />
  </svg>
);

export const Paper: React.FC<{x: number; y: number; w: number; h: number; color?: string; rotate?: number;
  ruled?: 'legal' | 'none'; children?: React.ReactNode; z?: number}> = ({x, y, w, h, color = C.paper, rotate = 0, ruled = 'none', children, z = 0}) => (
  <div style={{
    position: 'absolute', left: x, top: y, width: w, height: h, background: color, transform: `rotate(${rotate}deg) translateZ(${z}px)`,
    boxShadow: '0 30px 60px rgba(0,0,0,.55), 0 4px 10px rgba(0,0,0,.35)', overflow: 'hidden',
    backgroundImage: ruled === 'legal'
      ? `linear-gradient(90deg, transparent 62px, #d98c8c 62px, #d98c8c 64px, transparent 64px), repeating-linear-gradient(180deg, transparent 0 31px, ${C.legalLine} 31px 32px)`
      : undefined,
    backgroundPosition: ruled === 'legal' ? '0 0, 0 70px' : undefined,
  }}>
    <svg width={w} height={h} style={{position: 'absolute', inset: 0, opacity: 0.22, mixBlendMode: 'multiply'}}>
      <filter id={`fib${w}${h}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed={w % 13} /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width="100%" height="100%" filter={`url(#fib${w}${h})`} />
    </svg>
    <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(160deg, rgba(255,255,255,.18), rgba(0,0,0,.08))'}} />
    {children}
  </div>
);

/** Left-to-right pen reveal between frames a..b (a<0 = already written). */
export const Ink: React.FC<{a: number; b: number; children: React.ReactNode; style?: React.CSSProperties}> = ({a, b, children, style}) => {
  const f = useCurrentFrame();
  // a < 0: already written; a >= b: not written yet in this beat
  const p = a < 0 ? 100 : a >= b ? 0 : interpolate(f, [a, b], [0, 100], clamp);
  return <div style={{clipPath: `inset(-20% ${100 - p}% -20% -2%)`, whiteSpace: 'pre', ...style}}>{children}</div>;
};

export const Typed: React.FC<{a: number; cps?: number; text: string; caret?: boolean; style?: React.CSSProperties}> = ({a, cps = 14, text, caret, style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = a < 0 ? text.length : Math.max(0, Math.min(text.length, Math.floor(((f - a) / fps) * cps)));
  return <span style={{whiteSpace: 'pre', ...style}}>{text.slice(0, n)}{caret && <span style={{opacity: Math.floor(f / 12) % 2 ? 0 : 1}}>▍</span>}</span>;
};

export const Mark: React.FC<{a: number; b: number; d: string; color?: string; width?: number; style?: React.CSSProperties; w?: number; h?: number}> = ({
  a, b, d, color = C.red, width = 3, style, w = 400, h = 40,
}) => {
  const f = useCurrentFrame();
  const p = a < 0 ? 0 : a >= b ? 1 : interpolate(f, [a, b], [1, 0], {...clamp, easing: ease});
  return (
    <svg width={w} height={h} style={{position: 'absolute', overflow: 'visible', ...style}}>
      <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={p} />
    </svg>
  );
};

export const Illegible: React.FC<{lines: number; width: number; gap?: number; color?: string; seed?: number; opacity?: number}> = ({
  lines, width, gap = 30, color = C.ink, seed = 1, opacity = 0.55,
}) => (
  <svg width={width} height={lines * gap} style={{display: 'block', opacity}}>
    {Array.from({length: lines}, (_, i) => {
      const lw = width * (0.55 + 0.42 * rand(seed + i));
      let d = `M0 ${i * gap + gap * 0.6}`;
      for (let x = 8; x < lw; x += 8) d += ` Q${x - 4} ${i * gap + gap * 0.6 - 5 * rand(seed * 7 + x)} ${x} ${i * gap + gap * 0.6 + 1.5 * (rand(x + i) - 0.5)}`;
      return <path key={i} d={d} stroke={color} strokeWidth={2.2} fill="none" strokeLinecap="round" />;
    })}
  </svg>
);

export const wrap = (memory: boolean | undefined, node: React.ReactNode) => (memory ? <Memory>{node}</Memory> : <>{node}</>);
const pick = <T,>(m: Record<string, T>, beat: string | undefined, dflt: string): T => m[beat ?? dflt] ?? m[dflt];

/* ------------------------------------------------------------------ EHR chart (n006, n009, n016, n018, n020) */
const EHR_ORDER = ['arrival', 'complaint', 'name_blank', 'instructions', 'type'];
export const EhrChart: React.FC<Base> = ({dur, memory, beat = 'type'}) => {
  const f = useCurrentFrame();
  const k = EHR_ORDER.indexOf(beat);
  const glow = k === 0 ? interpolate(f, [0, 10], [0, 1], clamp) : 1;
  const focusRow = ['ARRIVAL', 'COMPLAINT', 'PATIENT', 'INSTRUCTIONS', 'PATIENT'][k];
  const p = interpolate(f, [0, dur], [0, 1], {...clamp, easing: ease});
  const rows: [string, React.ReactNode, number][] = [
    ['ARRIVAL', '03:05', 0],
    ['PATIENT', beat === 'type' ? <Typed a={8} cps={9} caret text="VESCARI, NICO" style={{fontFamily: F.type, fontSize: 26, color: '#fff'}} />
      : k >= 2 ? <Typed a={0} text="" caret /> : '', 0],
    ['COMPLAINT', k === 1 ? <Typed a={4} cps={22} text="Laceration, right volar forearm" /> : 'Laceration, right volar forearm', 1],
    ['PROCEDURE', 'Plaster splint, fingertips to elbow', 3],
    ['INSTRUCTIONS', k === 3 ? <Typed a={4} cps={14} text="Six weeks. No gripping." /> : 'Six weeks. No gripping.', 3],
    ['PROVIDER', 'MARLOWE, I., MD', 0],
  ];
  const focusIdx = rows.findIndex((r) => r[0] === focusRow);
  return wrap(memory,
    <AbsoluteFill style={{background: '#06090c'}}>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 30% 30%, rgba(40,90,110,.35), transparent 60%)'}} />
      <AbsoluteFill style={{transform: `scale(${1.04 + 0.12 * p + (k > 0 ? 0.12 : 0)}) rotateY(-6deg)`,
        transformOrigin: `42% ${30 + focusIdx * 8}%`, perspective: 1200, opacity: glow}}>
        <div style={{position: 'absolute', left: 150, top: 92, width: 900, height: 520, background: '#0d1820', borderRadius: 8,
          boxShadow: '0 0 80px rgba(70,150,200,.25), inset 0 0 0 2px #1b2c38', fontFamily: F.ui, overflow: 'hidden'}}>
          <div style={{background: '#16384a', color: '#cfe6f3', padding: '12px 18px', fontSize: 16, letterSpacing: 2}}>
            ST. BRIGID’S · EMERGENCY DEPARTMENT · BAY 14</div>
          <div style={{padding: '14px 10px'}}>
            {rows.map(([label, value, need], i) => (
              <div key={label} style={{display: 'flex', gap: 18, padding: '9px 14px', background: i === focusIdx ? 'rgba(80,170,255,.12)' : 'transparent',
                borderBottom: '1px solid rgba(160,200,230,.12)'}}>
                <div style={{width: 190, color: '#7fa6bf', fontSize: 17, letterSpacing: 1}}>{label}</div>
                <div style={{color: '#e7f2fa', fontSize: 21}}>{k >= need ? value : ''}</div>
              </div>
            ))}
          </div>
        </div>
        <div style={{position: 'absolute', left: 150, top: 92, width: 900, height: 520, pointerEvents: 'none',
          background: 'repeating-linear-gradient(180deg, rgba(255,255,255,.025) 0 2px, transparent 2px 4px)'}} />
      </AbsoluteFill>
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ Subpoena (n034, n038, n079) */
export const Subpoena: React.FC<Base> = ({dur, memory, beat = 'doc'}) => {
  const fr = pick<Frame>({doc: {fx: 50, fy: 40, zoom: 1.0, enter: true}, date: {fx: 46, fy: 62, zoom: 1.45}}, beat, 'doc');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr}>
      <Paper x={360} y={70} w={560} h={720} rotate={-2.5}>
        <div style={{padding: '46px 52px', fontFamily: F.type, color: '#222', fontSize: 15, lineHeight: 1.5}}>
          <div style={{textAlign: 'center', fontWeight: 700}}>UNITED STATES DISTRICT COURT</div>
          <div style={{textAlign: 'center'}}>EASTERN DISTRICT OF NEW YORK</div>
          <div style={{textAlign: 'center', marginTop: 18, fontWeight: 700, fontSize: 18, whiteSpace: 'pre'}}>SUBPOENA TO TESTIFY{'\n'}BEFORE A GRAND JURY</div>
          <div style={{marginTop: 26}}>To: <b>Dr. Ivy Marlowe</b></div>
          <div style={{marginTop: 18}}><Illegible lines={4} width={450} gap={22} color="#555" seed={3} opacity={0.35} /></div>
          <div style={{marginTop: 22, position: 'relative', fontSize: 21, fontWeight: 700}}>
            Thursday · 10:00 a.m.
            <Mark a={beat === 'date' ? 8 : -1} b={beat === 'date' ? 26 : 0} w={300} h={30} d="M0 30 C 80 34, 180 26, 285 31" style={{left: -4, top: 4}} />
          </div>
          <div style={{marginTop: 22}}><Illegible lines={5} width={450} gap={22} color="#555" seed={9} opacity={0.35} /></div>
        </div>
      </Paper>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Terms (n056, n059, n062, n088) */
const TERMS = ['One. I keep my residency, every shift.', 'Two. My own bedroom, with a lock on my side.', "Three. Theo's debt, gone tonight.",
  'Four. No one in his family touches me,\n        including his men.', 'Five. When the case is dead, we divorce.', 'Six. Not one cent of his money.',
  'Seven. You never lie to me.'];
const TERM_BEAT: Record<string, [number, number]> = {t1: [0, 0], t2: [1, 1], t3: [2, 2], t4: [3, 3], t5t6: [4, 5], t7: [6, 6]};
export const LegalPadTerms: React.FC<Base & {stage?: string}> = ({dur, memory, beat, stage}) => {
  const b = beat ?? (stage === 'seven' ? 't7' : 't5t6');
  const [from, to] = TERM_BEAT[b] ?? [6, 6];
  const tops = TERMS.map((t, i) => TERMS.slice(0, i).reduce((a, x) => a + (x.includes('\n') ? 96 : 64), 0));
  const focusY = 8 + ((tops[from] + 74) / 760) * 92;
  const per = (dur - 10) / (to - from + 1);
  const fr: Frame = {fx: 46, fy: Math.min(80, focusY), zoom: b === 't1' ? 1.15 : 1.3, enter: b === 't1', tilt: 14};
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#3a2a1e">
      <Paper x={300} y={30} w={680} h={760} color={C.legal} ruled="legal" rotate={1.5}>
        <div style={{position: 'absolute', left: 84, top: 74, fontFamily: F.hand, fontSize: 31, color: C.ink, lineHeight: '32px'}}>
          {TERMS.map((t, i) => i > to ? null : (
            <Ink key={i} a={i < from ? -1 : 4 + (i - from) * per} b={i < from ? 0 : 4 + (i - from) * per + per * 0.75}
              style={{height: t.includes('\n') ? 96 : 64, fontSize: i === 6 ? 36 : 31}}>{t}</Ink>
          ))}
        </div>
      </Paper>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Contract page eleven (n084, n085, n119, n155) */
export const ContractPage: React.FC<Base & {stage?: string}> = ({dur, memory, beat = 'line'}) => {
  const fin = beat === 'she_does' || beat === 'term_six';
  const fr = pick<Frame>({
    pages: {fx: 50, fy: 45, zoom: 0.92, enter: true}, line: {fx: 42, fy: 60, zoom: 1.35}, initials: {fx: 62, fy: 70, zoom: 1.5},
    leak: {fx: 50, fy: 92, zoom: 1.5, enter: true}, she_does: {fx: 42, fy: 70, zoom: 1.3, enter: true}, term_six: {fx: 44, fy: 82, zoom: 1.45},
  }, beat, 'line');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface={fin ? '#2b2220' : beat === 'leak' ? '#141414' : '#2a1d14'}>
      {(beat === 'pages' || beat === 'leak') && Array.from({length: 10}, (_, i) => (
        <Paper key={i} x={330 + (i + 1) * 9} y={20 + (i + 1) * 5} w={620} h={800} rotate={-1 + (i + 1) * 0.6} color="#efe8d8" z={-(i + 1) * 3}><div /></Paper>
      ))}
      <Paper x={330} y={20} w={620} h={800} rotate={-1}>
        <div style={{padding: '40px 56px', fontFamily: F.type, fontSize: 14, color: '#2a2a2a', lineHeight: 1.55}}>
          <div style={{fontWeight: 700, letterSpacing: 2}}>SECTION 4 · OBLIGATIONS OF NICO VESCARI</div>
          <div style={{marginTop: 14}}><Illegible lines={9} width={500} gap={21} color="#444" seed={21} opacity={0.4} /></div>
          {beat !== 'pages' && (
            <div style={{marginTop: 26, fontFamily: F.hand, fontSize: 33, color: '#1d1d1d', letterSpacing: 2, transform: 'rotate(-2deg) skewX(-6deg)', lineHeight: 1.1}}>
              <Ink a={beat === 'line' ? 6 : -1} b={beat === 'line' ? Math.min(dur * 0.8, 80) : 0}>SHE WILL LOOK LIKE{'\n'}SHE LOVES ME.</Ink>
            </div>
          )}
          {(beat === 'initials' || beat === 'leak' || fin) && (
            <Ink a={beat === 'initials' ? 6 : -1} b={beat === 'initials' ? 22 : 0}
              style={{fontFamily: F.hand, fontSize: 30, color: C.ink, marginTop: 10, marginLeft: 330}}>I.M.</Ink>
          )}
          {fin && (
            <div style={{fontFamily: F.hand, color: C.ink, marginTop: 6}}>
              <Ink a={beat === 'she_does' ? 10 : -1} b={beat === 'she_does' ? dur * 0.6 : 0} style={{fontSize: 40}}>She does.</Ink>
              {beat === 'term_six' && <Ink a={6} b={dur * 0.8} style={{fontSize: 31, marginTop: 10}}>Term six. Nobody in this house{'\n'}is quiet anymore.</Ink>}
            </div>
          )}
          <div style={{position: 'absolute', bottom: 30, left: 0, right: 0, textAlign: 'center', fontSize: 13}}>— 11 —</div>
          {beat === 'leak' && <Mark a={14} b={34} w={90} h={50} d="M8 26 C 14 4, 76 4, 82 26 C 76 48, 14 48, 8 26" style={{left: 265, bottom: 14}} />}
        </div>
      </Paper>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Joey's pocket schedule (n093, n094, n096) */
export const PocketSchedule: React.FC<Base> = ({dur, memory, beat = 'month'}) => {
  const fr = pick<Frame>({month: {fx: 50, fy: 35, zoom: 1.0, enter: true}, hand: {fx: 45, fy: 45, zoom: 1.6}, level2: {fx: 48, fy: 82, zoom: 1.5}}, beat, 'month');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#1e2224" lampX={55}>
      <Paper x={420} y={40} w={430} h={640} color="#f4f1e6" rotate={3}>
        <div style={{padding: '34px 38px', fontFamily: F.hand, color: C.ink}}>
          <div style={{fontSize: 34, transform: 'skewX(-12deg)'}}>October</div>
          <div style={{marginTop: 10, transform: 'skewX(-12deg)'}}><Illegible lines={12} width={340} gap={28} seed={33} opacity={0.75} /></div>
          <div style={{position: 'relative', marginTop: 18, fontSize: 36, transform: 'skewX(-12deg)'}}>
            Level 2. Space 2-14
            <Mark a={beat === 'level2' ? dur * 0.35 : -1} b={dur * 0.5} color={C.ink} width={2.5} w={300} h={24} d="M0 8 C 90 12, 200 4, 290 9" style={{left: 0, top: 44}} />
            <Mark a={beat === 'level2' ? dur * 0.55 : -1} b={dur * 0.7} color={C.ink} width={2.5} w={300} h={24} d="M4 16 C 100 19, 210 12, 284 16" style={{left: 0, top: 44}} />
          </div>
        </div>
      </Paper>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Ivy's phone (n098, n099, n130, n135, n141) */
export const PhoneNote: React.FC<Base & {stage?: string}> = ({dur, memory, beat, stage}) => {
  const f = useCurrentFrame();
  const b = beat ?? (stage === 'compare' ? 'compare' : 'note');
  const slide = interpolate(f, [0, 16], [40, 0], {...clamp, easing: ease});
  const phone = (x: number, title: string, children: React.ReactNode, lie = false) => (
    <div style={{position: 'absolute', left: x, top: 60 + slide, width: 330, height: 600, borderRadius: 42, background: '#0b0b0d',
      boxShadow: '0 40px 80px rgba(0,0,0,.7), inset 0 0 0 3px #2a2a2e', padding: 14, boxSizing: 'border-box',
      transform: lie ? 'perspective(900px) rotateX(48deg) translateY(60px)' : undefined}}>
      <div style={{width: '100%', height: '100%', borderRadius: 30, background: '#f7f5ef', overflow: 'hidden', fontFamily: F.ui}}>
        <div style={{padding: '18px 18px 10px', fontSize: 14, color: '#888', borderBottom: '1px solid #e2ddd2'}}>{title}</div>
        <div style={{padding: 18}}>{children}</div>
      </div>
    </div>
  );
  const call = (name: string, time: string, label: string) => (
    <div style={{textAlign: 'center', paddingTop: 60}}>
      <div style={{fontSize: 15, color: '#888'}}>{time}</div>
      <div style={{fontSize: 32, color: '#111', marginTop: 16}}>{name}</div>
      <div style={{fontSize: 15, color: '#888', marginTop: 8}}>{label}</div>
      <div style={{width: 64, height: 64, borderRadius: 32, margin: '120px auto 0', background: '#3aa55d',
        transform: `scale(${1 + 0.08 * Math.sin(f / 4)})`}} />
    </div>
  );
  const bubble = (t: React.ReactNode, a: number) => (
    <div style={{opacity: interpolate(f, [a, a + 8], [0, 1], clamp), background: '#e4e1d8', borderRadius: 16, padding: '10px 14px', fontSize: 17, color: '#222', marginBottom: 10, maxWidth: 250}}>{t}</div>
  );
  const NOTE = "Ivy, I'm sorry.\nI couldn't live with it.\nTell Danny I tried.";
  const marlowe = (seed: number, a: number) => bubble(<><b>Marlowe</b> — <Illegible lines={1} width={140} gap={18} color="#555" seed={seed} opacity={0.6} /></>, a);
  let body: React.ReactNode;
  if (b === 'call') body = phone(475, 'Incoming call', call('Priya', '6:41', 'mobile'));
  else if (b === 'brancato') body = phone(475, 'Incoming call', call('Carmine Brancato', '11:31', 'unknown number'));
  else if (b === 'call_nico') body = phone(475, 'Calling', call('Nico', '', 'calling…'));
  else if (b === 'speaker') body = phone(475, 'On call', call('Agent Reyes', '', 'speaker'), true);
  else if (b === 'note') body = phone(475, 'Notes', <div style={{fontSize: 21, lineHeight: 1.45, color: '#1a1a1a'}}><Typed a={10} cps={11} text={NOTE} /></div>);
  else if (b === 'texts') body = phone(475, 'Marcus Bell', <>{marlowe(41, 6)}{marlowe(44, 20)}{marlowe(47, 34)}</>);
  else body = <>
    {phone(170, 'Notes', <div style={{fontSize: 21, lineHeight: 1.45, color: '#1a1a1a'}}>{NOTE.split('\n').map((l) => <div key={l}>{l}</div>)}</div>)}
    {phone(780, 'Marcus Bell', <>{marlowe(41, -8)}{marlowe(44, -8)}{marlowe(47, -8)}</>)}
    <Mark a={dur * 0.3} b={dur * 0.5} color={C.red} width={3} w={90} h={60} d="M8 30 C 14 6, 70 6, 76 30 C 70 54, 14 54, 8 30" style={{left: 180, top: 120 + slide}} />
    <Mark a={dur * 0.55} b={dur * 0.75} color={C.red} width={3} w={120} h={40} d="M4 22 C 30 30, 80 30, 110 22" style={{left: 812, top: 142 + slide}} />
  </>;
  return wrap(memory,
    <AbsoluteFill style={{background: b === 'speaker' ? 'radial-gradient(ellipse at 50% 60%, #f3efe6, #9c9688 75%)' : 'radial-gradient(ellipse at 50% 40%, #2c3438, #08090a 70%)'}}>
      {body}
      <Dust count={14} opacity={0.25} />
    </AbsoluteFill>,
  );
};

/* ------------------------------------------------------------------ Lot 4471-B (n101, n110, n126) */
export const LotEvidence: React.FC<Base> = ({dur, memory, beat = 'link'}) => {
  const f = useCurrentFrame();
  const link = beat === 'link' ? interpolate(f, [dur * 0.25, dur * 0.55], [0, 1], {...clamp, easing: ease}) : 0;
  const fr = pick<Frame>({card: {fx: 24, fy: 66, zoom: 1.7, enter: true}, form: {fx: 72, fy: 32, zoom: 1.55}, link: {fx: 50, fy: 50, zoom: 1.0}}, beat, 'link');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#20262a" lampX={50}>
      <div style={{position: 'absolute', left: 120, top: 170, width: 330, height: 380, borderRadius: 10, transform: 'rotate(-6deg)',
        background: 'linear-gradient(135deg,#d9dde0,#9aa3a8 40%,#e8ecee 60%,#8f989d)', boxShadow: '0 30px 60px rgba(0,0,0,.6)'}}>
        {Array.from({length: 10}, (_, i) => (
          <div key={i} style={{position: 'absolute', left: 40 + (i % 2) * 130, top: 30 + Math.floor(i / 2) * 52, width: 110, height: 38, borderRadius: 19,
            background: 'radial-gradient(ellipse at 40% 30%, #fff, #b8c0c4 70%)', boxShadow: 'inset 0 -3px 6px rgba(0,0,0,.25)'}} />
        ))}
        <div style={{position: 'absolute', left: 30, bottom: 26, width: 270, background: '#fdfdf8', padding: '8px 12px', fontFamily: F.type, fontSize: 15, color: '#222', boxShadow: '0 2px 4px rgba(0,0,0,.3)'}}>
          OXYCODONE · 30 mg<br /><b style={{fontSize: 20}}>LOT 4471-B</b>
        </div>
      </div>
      <Paper x={640} y={60} w={520} h={640} rotate={2}>
        <div style={{padding: '36px 40px', fontFamily: F.type, fontSize: 15, color: '#222', lineHeight: 1.6}}>
          <div style={{fontWeight: 700, fontSize: 17, whiteSpace: 'pre'}}>CONTROLLED SUBSTANCE{'\n'}DESTRUCTION RECORD</div>
          <div style={{marginTop: 4}}>Hospital Pharmacy</div>
          <div style={{marginTop: 24}}>Date: <b>September 29</b></div>
          <div>Lot: <b style={{fontSize: 20}}>4471-B</b></div>
          <div>Quantity: <b>42 cards</b></div>
          <div style={{marginTop: 18}}><Illegible lines={4} width={420} gap={22} color="#555" seed={61} opacity={0.35} /></div>
          <div style={{marginTop: 26}}>Co-signed:</div>
          <div style={{fontFamily: F.hand, fontSize: 34, color: C.ink, marginTop: 2}}>Marcus Bell, MD</div>
        </div>
      </Paper>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
        <path d="M290 512 C 460 480, 560 280, 704 232" fill="none" stroke={C.red} strokeWidth={3} strokeDasharray="1" pathLength={1} strokeDashoffset={1 - link} strokeLinecap="round" />
        <ellipse cx={774} cy={226} rx={70} ry={20} fill="none" stroke={C.red} strokeWidth={2.5} opacity={link} />
      </svg>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Sal's ledger (n120, n125) */
export const Ledger: React.FC<Base> = ({dur, memory, beat = 'fl'}) => {
  const laid = beat === 'laid_out';
  const fr = pick<Frame>({cb: {fx: 45, fy: 40, zoom: 1.15, enter: true}, fl: {fx: 46, fy: 86, zoom: 1.55}, laid_out: {fx: 50, fy: 50, zoom: 0.8, enter: true}}, beat, 'fl');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface={laid ? '#d8d4ca' : '#111'} lampX={50}>
      <Paper x={300} y={40} w={680} h={660} color="#ece4d0" rotate={-1}>
        <div style={{padding: '30px 44px', fontFamily: F.hand, color: '#2a2a2a', fontSize: 27, lineHeight: '34px'}}>
          {Array.from({length: 14}, (_, i) => (
            <div key={i} style={{display: 'flex', gap: 40, opacity: 0.85}}>
              <Illegible lines={1} width={90} gap={34} color="#333" seed={70 + i} opacity={0.5} /><span>C.B.</span>
              <Illegible lines={1} width={120} gap={34} color="#333" seed={90 + i} opacity={0.5} />
            </div>
          ))}
          <div style={{marginTop: 10, fontSize: 34, color: '#111'}}><Ink a={beat === 'fl' ? dur * 0.2 : beat === 'cb' ? 9999 : -1} b={dur * 0.6}>Oct 1 — F.L. 20. Paid.</Ink></div>
        </div>
      </Paper>
      {laid && <>
        <Paper x={20} y={150} w={240} h={380} color="#fbfaf4" rotate={-7}>
          <div style={{padding: 20, fontFamily: F.type, fontSize: 14, color: '#333', lineHeight: 1.6}}>
            <div style={{textAlign: 'center', fontWeight: 700}}>DELI</div><Illegible lines={3} width={190} gap={18} color="#777" seed={131} opacity={0.4} />
            <div style={{marginTop: 8}}>1  PREPAID PHONE</div><Illegible lines={5} width={190} gap={18} color="#777" seed={137} opacity={0.4} />
          </div>
        </Paper>
        <div style={{position: 'absolute', left: 1010, top: 120, width: 300, height: 460, borderRadius: 18, transform: 'rotate(8deg)',
          background: 'linear-gradient(160deg,#c9a77a,#a8865a)', boxShadow: '0 30px 60px rgba(0,0,0,.35)'}}>
          <svg width={300} height={460} style={{opacity: 0.25}}><filter id="twill"><feTurbulence baseFrequency="0.6 0.05" numOctaves="2" seed="5" /></filter><rect width="100%" height="100%" filter="url(#twill)" /></svg>
        </div>
      </>}
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Bell's letter (n124) */
export const BellLetter: React.FC<Base> = ({dur, memory, beat = 'closing'}) => {
  const fr = pick<Frame>({letter: {fx: 50, fy: 40, zoom: 1.0, enter: true}, form_cash: {fx: 32, fy: 55, zoom: 1.1}, closing: {fx: 48, fy: 80, zoom: 1.5}}, beat, 'closing');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#3a3128" lampX={30}>
      {beat === 'form_cash' && (
        <Paper x={40} y={180} w={300} h={380} rotate={-6} color="#f4f1e8">
          <div style={{padding: 22, fontFamily: F.type, fontSize: 12, color: '#333', lineHeight: 1.6}}>
            <div style={{fontWeight: 700, whiteSpace: 'pre'}}>CONTROLLED SUBSTANCE{'\n'}DESTRUCTION RECORD</div>
            <div style={{marginTop: 10}}>Lot: <b>4471-B</b></div><Illegible lines={6} width={240} gap={18} color="#666" seed={15} opacity={0.35} />
            <div style={{fontFamily: F.hand, fontSize: 24, color: C.ink, marginTop: 8}}>Marcus Bell, MD</div>
          </div>
        </Paper>
      )}
      <Paper x={360} y={30} w={560} h={740} color={C.cream} rotate={1.2}>
        <div style={{padding: '50px 54px', fontFamily: F.serif, fontStyle: 'italic', color: '#2b2b44'}}>
          <Illegible lines={14} width={450} gap={30} color="#33334d" seed={111} opacity={0.5} />
          <div style={{marginTop: 18, fontSize: 36}}><Ink a={beat === 'closing' ? dur * 0.2 : beat === 'letter' ? 999 : 999} b={dur * 0.6}>Ivy, say it.{'\n'}Say all of it.</Ink></div>
          <div style={{marginTop: 18, fontSize: 30, marginLeft: 260, opacity: 0.85}}>Marcus</div>
        </div>
      </Paper>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ Receipt -> Paulie (n134, n136) */
export const EvidenceChain: React.FC<Base> = ({dur, memory, beat = 'link'}) => {
  const f = useCurrentFrame();
  const l1 = beat === 'receipt' ? 0 : beat === 'link' ? interpolate(f, [dur * 0.2, dur * 0.55], [0, 1], {...clamp, easing: ease}) : 1;
  const fr = pick<Frame>({receipt: {fx: 22, fy: 50, zoom: 1.5, enter: true}, link: {fx: 50, fy: 50, zoom: 1.0}, confessed: {fx: 78, fy: 45, zoom: 1.45}}, beat, 'link');
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#1d2326">
      <Paper x={150} y={150} w={260} h={420} color="#fbfaf4" rotate={-4}>
        <div style={{padding: 22, fontFamily: F.type, fontSize: 15, color: '#333', lineHeight: 1.6}}>
          <div style={{textAlign: 'center', fontWeight: 700}}>DELI</div><Illegible lines={3} width={210} gap={18} color="#777" seed={131} opacity={0.4} />
          <div style={{marginTop: 10}}>1  PREPAID PHONE</div><div>1  GUM</div><Illegible lines={4} width={210} gap={18} color="#777" seed={137} opacity={0.4} />
        </div>
      </Paper>
      <div style={{position: 'absolute', left: 440, top: 470, width: 150, height: 56, borderRadius: 6, transform: 'rotate(8deg)', background: 'linear-gradient(180deg,#2f8f5b,#1f6b42)', boxShadow: '0 16px 30px rgba(0,0,0,.5)'}} />
      <Paper x={830} y={230} w={300} h={180} color="#efe9da" rotate={2}>
        <div style={{padding: '50px 26px', fontFamily: F.type, fontSize: 24, fontWeight: 700, color: '#222', opacity: l1}}>PAULIE FERRARO</div>
      </Paper>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <path d="M410 330 C 560 300, 700 330, 830 320" stroke={C.red} strokeWidth={beat === 'confessed' ? 4 : 3} fill="none" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - l1} />
        <path d="M560 490 C 650 450, 740 400, 830 360" stroke={C.red} strokeWidth={beat === 'confessed' ? 4 : 3} fill="none" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - l1} />
      </svg>
    </DeskScene>,
  );
};

/* ------------------------------------------------------------------ The cream envelope (n147, n154) */
export const DivorceEnvelope: React.FC<Base> = ({dur, memory, beat = 'pages'}) => {
  const f = useCurrentFrame();
  const env = beat === 'envelope' || beat === 'envelope2';
  const fr = pick<Frame>({envelope: {fx: 50, fy: 50, zoom: 1.0, enter: true}, envelope2: {fx: 50, fy: 52, zoom: 1.2, enter: true},
    pages: {fx: 46, fy: 30, zoom: 1.25, enter: true}, signature: {fx: 40, fy: 62, zoom: 1.6}}, beat, 'pages');
  const set = beat === 'envelope' ? interpolate(f, [0, 20], [-60, 0], {...clamp, easing: ease}) : 0;
  return wrap(memory,
    <DeskScene dur={dur} frame={fr} surface="#2a2522" lampX={45}>
      {env ? (
        <div style={{position: 'absolute', left: 300, top: 180 + set, width: 680, height: 400, background: C.cream, borderRadius: 4, boxShadow: '0 30px 60px rgba(0,0,0,.55)'}}>
          <svg width={680} height={400} style={{position: 'absolute'}}><path d="M0 0 L340 220 L680 0" stroke="#d6c9ac" strokeWidth={3} fill="none" /></svg>
        </div>
      ) : <>
        <Paper x={392} y={46} w={520} h={680} rotate={-2} color="#f6f2e8" z={-4}><div /></Paper>
        <Paper x={388} y={43} w={520} h={680} rotate={-1.2} color="#f7f3ea" z={-2}><div /></Paper>
        <Paper x={384} y={40} w={520} h={680} rotate={-0.5} color="#f8f5ec">
          <div style={{padding: '40px 48px', fontFamily: F.type, fontSize: 15, color: '#222', lineHeight: 1.6}}>
            <div style={{fontWeight: 700, fontSize: 19}}>TERM FIVE</div>
            <div style={{marginTop: 14}}><Illegible lines={12} width={420} gap={22} color="#555" seed={151} opacity={0.35} /></div>
            <div style={{marginTop: 40, borderTop: '1px solid #444', width: 260}} />
            <Ink a={beat === 'signature' ? dur * 0.15 : 9999} b={dur * 0.9} style={{fontFamily: F.hand, fontSize: 40, color: C.ink, transform: 'rotate(-3deg) translateY(-58px)'}}>N. Vescari</Ink>
          </div>
          <div style={{position: 'absolute', left: 30, top: 18, width: 26, height: 7, background: '#9aa', transform: 'rotate(-30deg)'}} />
        </Paper>
      </>}
    </DeskScene>,
  );
};
