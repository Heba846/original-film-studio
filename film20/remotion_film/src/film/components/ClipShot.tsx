import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {FPS} from '../theme';
import {Memory} from './Atmosphere';

/** Named crops. All scales are >= 1 and positive: footage is never flipped
 *  (injured arm = RIGHT, eyebrow scar = LEFT). */
export const CROPS: Record<string, {scale: number; x: number; y: number}> = {
  full: {scale: 1.0, x: 0, y: 0},
  reaction: {scale: 1.25, x: -0.12, y: -0.05},
  detail: {scale: 1.4, x: 0, y: 0.08},
  ivy: {scale: 1.3, x: -0.15, y: -0.04},
  wide: {scale: 1.0, x: 0, y: 0},
  // planning names for crops on not-yet-delivered takes; tuned once the real frame exists
  theo: {scale: 1.25, x: 0.1, y: -0.03},
  sal: {scale: 1.25, x: -0.1, y: -0.04},
  nico: {scale: 1.25, x: 0.08, y: -0.04},
};

/** Pixel-rectangle crops on delivered 1280x720 takes: [x0, y0, width]; height = width*9/16.
 *  Plain 720p crop + scale (no AI upscaling). Scale above 2x is flagged soft in STATUS.md. */
export const RECTS: Record<string, [number, number, number]> = {
  f07_eyes: [416, 164, 448],   // eyes only: no wiper/dashboard, geography-neutral listener shot
  f09_face: [464, 156, 512],   // between the two white figures
  f10_hands: [130, 360, 640],  // wound + gloved hands insert
  f12_ivy: [20, 40, 640],      // Ivy only; excludes the white wrap at his wrist
};
const rectToCrop = ([x0, y0, w]: [number, number, number]) => {
  const s = 1280 / w, cx = x0 + w / 2, cy = y0 + (w * 9) / 32;
  return {scale: s, x: (-s * (cx - 640)) / 1280, y: (-s * (cy - 360)) / 720};
};

export type ClipProps = {
  src: string; // relative to public/
  inS: number; // resolved by tools/film_build.py
  rate: number; // resolved by tools/film_build.py (0.85-1.0); never retimed here
  dur: number; // frames on screen (incl. outgoing dissolve)
  crop?: string;
  memory?: boolean;
  drift?: 'in' | 'out' | 'left' | 'right';
};

export const ClipShot: React.FC<ClipProps> = ({src, inS, rate, dur, crop = 'full', memory, drift = 'in'}) => {
  const f = useCurrentFrame();
  const c = RECTS[crop] ? rectToCrop(RECTS[crop]) : CROPS[crop] ?? CROPS.full;
  if (c.scale <= 0) throw new Error('Negative/zero scale would flip footage: forbidden');
  if (rate < 0.85 - 1e-6 || rate > 1 + 1e-6) throw new Error(`playback rate ${rate} outside 0.85-1.0`);
  const p = interpolate(f, [0, dur], [0, 1], {extrapolateRight: 'clamp'});
  // restrained parallax: <= 3% scale change, <= 1.2% lateral drift
  const ds = drift === 'out' ? 0.03 * (1 - p) : drift === 'in' ? 0.03 * p : 0.015;
  const dx = drift === 'left' ? -0.012 * p : drift === 'right' ? 0.012 * p : 0;
  const video = (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: 'black'}}>
      <OffthreadVideo src={staticFile(src)} startFrom={Math.round(inS * FPS)} playbackRate={rate} muted
        style={{width: '100%', height: '100%', objectFit: 'cover', transform: `translate(${(c.x + dx) * 100}%, ${c.y * 100}%) scale(${c.scale + ds})`}} />
    </AbsoluteFill>
  );
  return memory ? <Memory>{video}</Memory> : video;
};
