import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import timeline from './data/film_timeline.json';
import {ClipShot} from './components/ClipShot';
import {CODE_COMPONENTS} from './components/registry';
import {Placeholder} from './components/Placeholder';
import {StillAnimatic} from './components/StillAnimatic';
import approvedStills from './data/approved_stills.json';
const STILLS = approvedStills as Record<string, string>;
import {Finish, Memory} from './components/Atmosphere';
import {Captions, ChapterTitle, DateStamp, Hud, Cue} from './components/Overlays';
import {STAMPS} from './stamps';

type Cut = {seg: string; chapter: string; from: number; dur: number; shot: string; slug?: string; kind: string; status: string;
  src_in?: number; src_out?: number; rate?: number; overlap: number; unresolved_f?: number; memory?: boolean; crop?: string;
  beat?: string; stage?: string; use_no?: number; is_reuse?: boolean; why?: string; chapter_open?: boolean};
type Shot = {kind: string; source?: string; status: string; component?: string; narrative_event: string; window?: number[];
  window_is_estimate?: boolean; on_disk?: boolean};
type Seg = {id: string; speaker: string; chapter: string; text: string; audio_status: string; audio: string | null; from: number; dur: number;
  cover_from: number; cover_dur: number};

export type TLType = {fps: number; total_frames: number; total_s: number; runtime_is_estimate: boolean;
  segments: Seg[]; cuts: Cut[]; chapters: {id: string; title: string; from: number; end_from: number}[]; captions: Cue[];
  shots: Record<string, Shot>; gate: {final_export_allowed: boolean; audio_missing: string[]; visual_shots_pending: string[];
  unresolved_frames: number; problems: string[]};
  variant?: {tag: string; start: number; end: number; approved_only: boolean; not_real_picture: string[]}};
export const TL = timeline as unknown as TLType;
const DONE = new Set(['approved', 'code']);

/** strict = true: any unfinished picture throws (Final master, approved-only scenes). */
const CutVisual: React.FC<{c: Cut; strict: boolean; tl: TLType}> = ({c, strict, tl}) => {
  const sh = tl.shots[c.shot];
  const seg = tl.segments.find((x) => x.id === c.seg)!;
  const body = c.dur - (c.unresolved_f ?? 0);
  if (!sh || !DONE.has(sh.status) || (sh.kind !== 'code' && !sh.on_disk)) {
    if (strict) throw new Error(`Strict render reached unfinished picture ${c.shot} (${c.seg})`);
    if (STILLS[c.shot]) return <StillAnimatic src={STILLS[c.shot]} dur={c.dur + c.overlap} shotId={c.shot} slug={c.slug} />;
    const plan = sh && sh.kind !== 'code' ? `planned ${c.src_in?.toFixed(2)}–${c.src_out?.toFixed(2)} s @ ${c.rate?.toFixed(3)}x · ${(c.dur / 24).toFixed(2)} s on screen`
      + (sh.window_is_estimate ? ' · window is an ESTIMATE (file not delivered)' : '') : undefined;
    return <Placeholder shotId={c.shot} slug={c.slug} event={sh?.narrative_event ?? 'undefined shot'} status={sh?.status ?? 'missing'}
      segment={c.seg} speaker={seg.speaker} text={seg.text} plan={plan} reuse={c.is_reuse ? c.why : undefined} memory={c.memory} />;
  }
  if (sh.kind === 'code') {
    const Comp = CODE_COMPONENTS[sh.component!];
    return <Comp dur={c.dur + c.overlap} memory={c.memory} beat={c.beat} stage={c.stage} />;
  }
  if (strict && (c.unresolved_f ?? 0) > 0) throw new Error(`Strict render reached unresolved frames in ${c.seg}`);
  return (
    <>
      <Sequence durationInFrames={body + c.overlap} layout="none">
        <ClipShot src={sh.source!} inS={c.src_in ?? 0} rate={c.rate ?? 1} dur={body + c.overlap} crop={c.crop} memory={c.memory} />
      </Sequence>
      {(c.unresolved_f ?? 0) > 0 && (
        <Sequence from={body} durationInFrames={c.unresolved_f!} layout="none">
          <Placeholder unresolved shotId={c.shot} slug={c.slug} event="source ends before this cut does" status="unresolved"
            segment={c.seg} speaker={seg.speaker} text={seg.text} />
        </Sequence>
      )}
    </>
  );
};

const Fade: React.FC<{children: React.ReactNode; inFrames: number}> = ({children, inFrames}) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{opacity: inFrames <= 1 ? 1 : interpolate(f, [0, inFrames], [0, 1], {extrapolateRight: 'clamp'})}}>{children}</AbsoluteFill>;
};

/** Renders frames [start, end) of a timeline.
 *  workbench: placeholders + HUD + burned captions; scene: strict (approved/code only) + burned captions, no HUD;
 *  final: strict, no captions (SRT ships separately). */
export const FilmTimeline: React.FC<{start: number; end: number; mode: 'workbench' | 'final' | 'scene'; label: string; tl?: TLType}> = ({
  start, end, mode, label, tl = TL,
}) => {
  const f = useCurrentFrame();
  const abs = f + start;
  const strict = mode !== 'workbench';
  const cuts = tl.cuts.filter((c) => c.from + c.dur + c.overlap > start && c.from < end);
  const segs = tl.segments.filter((s) => s.from + s.dur > start && s.from < end);
  const cur = tl.cuts.find((c) => abs >= c.from && abs < c.from + c.dur);
  const curSeg = cur ? tl.segments.find((s) => s.id === cur.seg) : undefined;
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      {cuts.map((c, i) => {
        const prev = tl.cuts[tl.cuts.indexOf(c) - 1];
        const fadeIn = c.chapter_open && c.from > 0 ? 14 : prev?.overlap ?? 0;
        return (
          <Sequence key={`${c.seg}-${i}`} from={c.from - start} durationInFrames={c.dur + c.overlap} layout="none">
            <Fade inFrames={fadeIn}><CutVisual c={c} strict={strict} tl={tl} /></Fade>
          </Sequence>
        );
      })}
      <Finish />
      {segs.map((s) => s.audio ? (
        <Sequence key={`a-${s.id}`} from={s.from - start} durationInFrames={s.dur} layout="none"><Audio src={staticFile(s.audio)} /></Sequence>
      ) : null)}
      {segs.filter((s) => STAMPS[s.id]).map((s) => (
        <Sequence key={`d-${s.id}`} from={s.from - start} durationInFrames={Math.min(s.cover_dur, 96)} layout="none">
          <DateStamp text={STAMPS[s.id]} dur={Math.min(s.cover_dur, 96)} />
        </Sequence>
      ))}
      {tl.chapters.filter((c) => c.from >= start && c.from < end && c.id !== 'CH00').map((c) => (
        <Sequence key={`c-${c.id}`} from={c.from - start + 8} durationInFrames={90} layout="none"><ChapterTitle title={c.title} dur={90} /></Sequence>
      ))}
      {mode !== 'final' && <Captions cues={tl.captions} offsetS={start / tl.fps} fps={tl.fps} />}
      {mode === 'workbench' && <Hud seg={curSeg} block={cur ? {shot: cur.slug ? `${cur.shot} ${cur.slug}` : cur.shot, status: tl.shots[cur.shot]?.status ?? 'missing',
        short_s: (cur.unresolved_f ?? 0) / 24} : undefined} tS={abs / tl.fps} totalS={tl.total_s} estimate={tl.runtime_is_estimate} label={label} />}
    </AbsoluteFill>
  );
};
export {Memory};
