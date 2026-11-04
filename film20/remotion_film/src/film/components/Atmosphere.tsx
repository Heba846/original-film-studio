import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {H, W, rand} from '../theme';

/** Film grain: SVG turbulence re-seeded every 2 frames (frame-deterministic). */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.09}) => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 2) % 97;
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity}}>
      <svg width={W} height={H}>
        <filter id={`g${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={seed} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

export const Vignette: React.FC<{strength?: number}> = ({strength = 0.55}) => (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background: `radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 52%, rgba(0,0,0,${strength}) 100%)`,
    }}
  />
);

/** Sodium-light flicker: a faint warm wash that dips irregularly (garage, night exteriors). */
export const Flicker: React.FC<{color?: string; amount?: number}> = ({color = '#e89a3c', amount = 0.08}) => {
  const f = useCurrentFrame();
  const r = rand(Math.floor(f / 3));
  const dip = r > 0.93 ? 0.5 : 1;
  return <AbsoluteFill style={{pointerEvents: 'none', background: color, mixBlendMode: 'soft-light', opacity: amount * dip}} />;
};

/** Window-pane rain: slanted streaks, deterministic, for exteriors/windows only (never indoors). */
export const Rain: React.FC<{density?: number; opacity?: number}> = ({density = 90, opacity = 0.35}) => {
  const f = useCurrentFrame();
  const drops = Array.from({length: density}, (_, i) => {
    const x = rand(i + 1) * (W + 200) - 100;
    const speed = 28 + rand(i + 7) * 22;
    const len = 18 + rand(i + 13) * 30;
    const y = ((rand(i + 3) * H + f * speed) % (H + 80)) - 40;
    return <line key={i} x1={x} y1={y} x2={x - len * 0.18} y2={y + len} stroke="white" strokeWidth={1} strokeOpacity={0.25 + rand(i) * 0.5} />;
  });
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity}}>
      <svg width={W} height={H}>{drops}</svg>
    </AbsoluteFill>
  );
};

/** Dust motes drifting in a light beam (study, courtroom, Bay 14 lamp). */
export const Dust: React.FC<{count?: number; opacity?: number}> = ({count = 40, opacity = 0.5}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity}}>
      <svg width={W} height={H}>
        {Array.from({length: count}, (_, i) => {
          const x = (rand(i + 2) * W + Math.sin((f + i * 30) / 70) * 30 + f * 0.15) % W;
          const y = (rand(i + 5) * H - f * (0.12 + rand(i) * 0.25) + H) % H;
          const r = 0.8 + rand(i + 9) * 1.8;
          return <circle key={i} cx={x} cy={y} r={r} fill="#fff6e0" fillOpacity={0.25 + 0.4 * rand(i + 11)} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Memory treatment: desaturate + bloom + soft edge pulse. Wraps children. */
export const Memory: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const pulse = interpolate(Math.sin(f / 9), [-1, 1], [0.04, 0.1]);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{filter: 'saturate(0.35) contrast(1.08) brightness(0.92) sepia(0.15)'}}>{children}</AbsoluteFill>
      <AbsoluteFill style={{background: 'white', mixBlendMode: 'screen', opacity: pulse}} />
      <Vignette strength={0.8} />
    </AbsoluteFill>
  );
};

/** Global finishing stack for every finished frame. */
export const Finish: React.FC = () => (
  <>
    <Vignette />
    <Grain />
  </>
);
