#!/usr/bin/env python3
"""Procedural (self-generated, no third-party samples) sound bed for the Opening Cinematic v2 sample.
Every event is tied to a picture moment in film_timeline_cinematic_v2.json. Output: output/cinematic_v2/sfx.wav (48 kHz stereo)."""
import numpy as np, wave
from pathlib import Path
SR = 48000; DUR = 1813 / 24; N = int(DUR * SR)
rng = np.random.default_rng(20)
t = np.arange(N) / SR
def db(x): return 10 ** (x / 20)
def lp(x, fc):  # one-pole lowpass (applied twice)
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for _ in range(2):
        for i in range(len(x)): s = a * s + (1 - a) * x[i]; y[i] = s
        x = y.copy()
    return y
def hp(x, fc): return x - lp(x, fc)
def env(a, b, fade):  # 0..1 gain curve: 1 inside [a,b], linear fades
    g = np.clip((t - a) / fade, 0, 1) * np.clip((b - t) / fade, 0, 1); return g
def ir(sec, damp):  # simple diffuse room impulse response
    n = int(sec * SR); return rng.standard_normal(n) * np.exp(-np.arange(n) / (damp * SR)) * 0.06
def place(buf, x, at, g):
    i = int(at * SR); j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
def verb(x, r): return np.convolve(x, r)[:len(x) + len(r) - 1]
# --- beds (computed on a shorter grid then repeated to keep this fast)
def loop(sig_fn, sec=8.0):
    m = int(sec * SR); s = sig_fn(m); f = int(0.5 * SR)
    s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
    out = np.zeros(N + m); k = 0
    while k < N: out[k:k + m] += s; k += m - f
    return out[:N]
garage = loop(lambda m: lp(np.cumsum(rng.standard_normal(m)) * 0.02 - 0, 220) )
garage = hp(garage, 25); garage /= np.sqrt(np.mean(garage ** 2)) + 1e-9
hum = (np.sin(2 * np.pi * 120 * t) + 0.35 * np.sin(2 * np.pi * 240 * t)) * (1 + 0.1 * np.sin(2 * np.pi * 0.3 * t))
er = loop(lambda m: lp(hp(rng.standard_normal(m), 180), 1800))
er /= np.sqrt(np.mean(er ** 2)) + 1e-9
fluor = np.sin(2 * np.pi * 120 * t) * 0.5 + 0.2 * np.sin(2 * np.pi * 360 * t)
# gain automation (seconds): garage present until the ER; dips under the bay-14 flashback, near-silence after "never here",
# J-cut: ER air fades in 0.5 s BEFORE the picture cut at 37.42; L-cut: garage tail lingers 0.4 s after it
G = (env(-1, 37.8, 0.6))
G *= 1 - 0.75 * env(24.95, 28.40, 0.25)               # flashback: the garage recedes
G *= 1 - 0.97 * env(31.25, 33.15, 0.35)               # near-silence beat after "You were never here."
G *= 1 - 0.6 * env(34.70, 37.40, 0.3)                 # flash-forward to the wedding: garage recedes
E_ = env(36.92, DUR + 1, 0.5) + 0.55 * env(24.95, 28.40, 0.25)   # ER air: present in the ER, and inside the flashback
bed = garage * db(-44) * G + hum * db(-58) * G + er * db(-47) * E_ + fluor * db(-63) * E_
fx = np.zeros(N + SR * 2)
rg, rer = ir(0.9, 0.28), ir(0.35, 0.08)               # concrete garage vs. treated ER
def drip(at, g):
    n = int(0.05 * SR); k = np.arange(n) / SR; f = 1700 + 900 * k / 0.05
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k / 0.012); place(fx, verb(x, rg), at, g)
def step(at, g, room):
    n = int(0.09 * SR); k = np.arange(n) / SR
    x = lp(rng.standard_normal(n), 900) * np.exp(-k / 0.018) * 3 + np.sin(2 * np.pi * 85 * k) * np.exp(-k / 0.025) * 0.5
    place(fx, verb(x, room), at, g)
def cloth(at, sec, g):
    n = int(sec * SR); x = hp(lp(rng.standard_normal(n), 5000), 900) * np.hanning(n); place(fx, x, at, g)
def key(at, g):
    n = int(0.012 * SR); x = hp(rng.standard_normal(n), 2500) * np.exp(-np.arange(n) / (0.002 * SR)); place(fx, verb(x, rer), at, g)
def door_close(at, g):
    n = int(0.7 * SR); k = np.arange(n) / SR; x = lp(hp(rng.standard_normal(n), 1200), 5000) * np.sin(np.pi * k / 0.7) ** 2
    place(fx, x, at, g); step(at + 0.68, g * 0.5, rer)
for a in (2.95, 9.2, 14.1, 20.6): drip(a, db(-27))     # sparse drips; the first lands in the pause after "Two shots."
drip(32.4, db(-33))                                     # one drip inside the near-silence
cloth(5.3, 0.45, db(-36)); cloth(11.65, 0.5, db(-34))   # Ivy shifts behind the bumper; rises to look over the hood
for a in (33.55, 34.12): step(a, db(-30), rg)           # "I went back inside": two steps as she turns to the stairwell door
door_close(37.75, db(-38))                              # ER sliding doors close behind him (F08 opens in the doorway)
for i in range(13): step(38.2 + i * 0.64, db(-31) * (0.85 + 0.3 * rng.random()), rer)   # his steps across the waiting room
for i, a in enumerate((72.98, 73.10, 73.19, 73.33, 73.45)): key(a, db(-30))         # the name typed into the chart: "Nico."
mix = bed + fx[:N]
peak = np.max(np.abs(mix)); assert peak < db(-12), peak
st = np.stack([mix, mix], 1)
out = Path(__file__).resolve().parents[2] / "output/cinematic_v2/sfx.wav"
with wave.open(str(out), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
print(out, f"peak {20*np.log10(peak):.1f} dBFS")
