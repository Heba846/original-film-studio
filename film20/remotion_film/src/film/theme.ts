import {continueRender, delayRender, staticFile} from 'remotion';

export const FPS = 24;
export const W = 1280;
export const H = 720;

export const C = {
  ink: '#1f3f8f', // blue ballpoint / fountain ink
  inkFaded: '#3b5aa8',
  pencil: '#3a3a3a',
  paper: '#f2ead8',
  paperShade: '#d9cdb2',
  legal: '#f6e98e',
  legalLine: '#9bb8d9',
  cream: '#efe4cc',
  sodium: '#e89a3c',
  teal: '#1d4b52',
  night: '#0d1012',
  red: '#b3352b',
  white: '#f5f3ee',
};

export const F = {
  hand: "'OFS Caveat', 'Comic Sans MS', cursive",
  type: "'OFS Courier Prime', 'Courier New', monospace",
  serif: "'OFS Cormorant', Georgia, serif",
  ui: "Inter, 'Helvetica Neue', Arial, sans-serif",
};

// Fonts ship inside public/fonts so renders never depend on the network.
const faces: [string, string, string, string][] = [
  ['OFS Caveat', 'fonts/caveat-latin-500-normal.woff2', '500', 'normal'],
  ['OFS Courier Prime', 'fonts/courier-prime-latin-400-normal.woff2', '400', 'normal'],
  ['OFS Courier Prime', 'fonts/courier-prime-latin-700-normal.woff2', '700', 'normal'],
  ['OFS Cormorant', 'fonts/cormorant-garamond-latin-500-normal.woff2', '500', 'normal'],
  ['OFS Cormorant', 'fonts/cormorant-garamond-latin-500-italic.woff2', '500', 'italic'],
];
if (typeof document !== 'undefined') {
  const handle = delayRender('Loading local fonts');
  Promise.all(
    faces.map(([family, file, weight, style]) => {
      const face = new FontFace(family, `url(${staticFile(file)}) format('woff2')`, {weight, style});
      return face.load().then((f) => document.fonts.add(f));
    }),
  )
    .then(() => continueRender(handle))
    .catch((e) => {
      console.error(e);
      continueRender(handle);
    });
}

/** Deterministic pseudo-random in [0,1) for frame-stable effects. */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};
