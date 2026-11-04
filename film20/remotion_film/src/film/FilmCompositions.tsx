import React from 'react';
import {AbsoluteFill, Composition, Sequence} from 'remotion';
import {FilmTimeline, TL, TLType} from './FilmTimeline';
import approvedOpening from './data/film_timeline_approved_opening.json';
import {CODE_COMPONENTS} from './components/registry';
import {Finish} from './components/Atmosphere';
import {F} from './theme';
import './theme';

const ch = (id: string) => TL.chapters.find((c) => c.id === id)!;
const CH00 = {start: 0, end: ch('CH00').end_from};
const CH01 = {start: ch('CH01').from, end: ch('CH01').end_from};

const AO = approvedOpening as unknown as TLType;
/** ~2:04 continuous scene: ONLY approved footage + finished code + complete narration (strict: placeholders throw). Not the film. */
const SceneApprovedOpening: React.FC = () => {
  if (!AO.variant?.approved_only) throw new Error('approved_opening variant is not approved-only: ' + AO.variant?.not_real_picture.join(', '));
  return <FilmTimeline start={AO.variant.start} end={AO.variant.end} mode="scene" label="" tl={AO} />;
};
const Workbench: React.FC = () => <FilmTimeline start={0} end={TL.total_frames} mode="workbench" label="WORKBENCH" />;
const EditorCH00: React.FC = () => <FilmTimeline start={CH00.start} end={CH00.end} mode="workbench" label="EDITOR PREVIEW · CH00 · NOT A FINISHED SCENE" />;
const TestCH01: React.FC = () => <FilmTimeline start={CH01.start} end={CH01.end} mode="workbench" label="TEST CH01 · 3:05" />;

/** Export gate: rendering the master fails on frame 0 while anything required is missing. */
const Final: React.FC = () => {
  const g = TL.gate;
  if (!g.final_export_allowed) {
    throw new Error(
      `Film20-Final export BLOCKED: ${g.audio_missing.length} pickups missing (${g.audio_missing.join(', ')}), ` +
        `${g.visual_shots_pending.length} shots not approved, ${g.unresolved_frames} unresolved frames, ` +
        `${g.problems.length} build problems. See edition20/out/STATUS.md.`,
    );
  }
  return <FilmTimeline start={0} end={TL.total_frames} mode="final" label="" />;
};

/** Evidence samples exactly as the timeline stages them: one entry per beat, at the beat's real length. */
const SAMPLE_SEGS = ['n020', 'n029', 'n031', 'n056', 'n084', 'n093', 'n099', 'n109', 'n110', 'n120', 'n124', 'n151', 'n155', 'n159'];
const SAMPLES = TL.cuts.filter((c) => SAMPLE_SEGS.includes(c.seg) && TL.shots[c.shot]?.kind === 'code');
const SAMPLE_STARTS = SAMPLES.reduce<number[]>((a, c, i) => [...a, i === 0 ? 0 : a[i - 1] + SAMPLES[i - 1].dur], []);
const SAMPLE_TOTAL = SAMPLES.reduce((a, c) => a + c.dur, 0);
const Gallery: React.FC = () => (
  <AbsoluteFill style={{background: 'black'}}>
    {SAMPLES.map((c, i) => {
      const Comp = CODE_COMPONENTS[TL.shots[c.shot].component!];
      return (
        <Sequence key={i} from={SAMPLE_STARTS[i]} durationInFrames={c.dur}>
          <Comp dur={c.dur} beat={c.beat} memory={c.memory} />
          <Finish />
          <div style={{position: 'absolute', left: 10, bottom: 8, fontFamily: F.ui, fontSize: 14, color: '#f2c200', background: 'rgba(0,0,0,.7)', padding: '3px 8px'}}>
            EVIDENCE SAMPLE · {c.seg} · {c.shot} · beat “{c.beat}” · {(c.dur / 24).toFixed(1)} s (narration is in the workbench)
          </div>
        </Sequence>
      );
    })}
  </AbsoluteFill>
);

export const FilmCompositions: React.FC = () => (
  <>
    <Composition id="Film20-Workbench" component={Workbench} durationInFrames={TL.total_frames} fps={TL.fps} width={1280} height={720} />
    <Composition id="Film20-Editor-CH00" component={EditorCH00} durationInFrames={CH00.end - CH00.start} fps={TL.fps} width={1280} height={720} />
    <Composition id="Film20-Test-CH01" component={TestCH01} durationInFrames={CH01.end - CH01.start} fps={TL.fps} width={1280} height={720} />
    <Composition id="Evidence-Gallery" component={Gallery} durationInFrames={SAMPLE_TOTAL} fps={TL.fps} width={1280} height={720} />
    <Composition id="Scene-ApprovedOnly-Opening" component={SceneApprovedOpening}
      durationInFrames={(AO.variant?.end ?? 1) - (AO.variant?.start ?? 0)} fps={TL.fps} width={1280} height={720} />
    <Composition id="Film20-Final" component={Final} durationInFrames={TL.total_frames} fps={TL.fps} width={1280} height={720} />
  </>
);
