from pathlib import Path
import os, json, subprocess, shutil, wave, zipfile
ROOT = Path(__file__).resolve().parent
FF = os.environ.get('OFS_FFMPEG') or shutil.which('ffmpeg')
if not FF: raise SystemExit('FFmpeg is required')
P = json.loads((ROOT/'timeline.json').read_text())
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
TMP=ROOT/'render_cache'; TMP.mkdir(exist_ok=True)
def run(args):
 subprocess.run([FF,'-y','-v','error',*map(str,args)],check=True)
def fr(s): return round(s*P['fps'])
for i,s in enumerate(P['shots']):
 width=round(1280*s['scale']/2)*2
 height=round(720*s['scale']/2)*2
 x='0' if s['origin'].startswith('left') else '(iw-1280)/2'
 vf=f'scale={width}:{height},crop=1280:720:{x}:(ih-720)/2,setsar=1,fps=24'
 run(['-ss',s['sourceStart'],'-i',ROOT/'public'/s['file'],'-vf',vf,'-frames:v',fr(s['end'])-fr(s['start']),'-an','-c:v','libx264','-preset','fast','-crf','20',TMP/f'{i}.mp4'])
(TMP/'concat.txt').write_text(''.join(f"file '{i}.mp4'\n" for i in range(len(P['shots']))))
run(['-f','concat','-safe','0','-i',TMP/'concat.txt','-c','copy',TMP/'video.mp4'])
args=[]; filters=[]; labels=[]
for i,a in enumerate(P['audio']):
 args+=['-i',ROOT/'public'/a['file']]
 ms=fr(a['start'])/24*1000
 filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={round(ms)}:all=1[a{i}]')
 labels.append(f'[a{i}]')
filters.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,apad,atrim=duration=16[out]')
run([*args,'-filter_complex',';'.join(filters),'-map','[out]',TMP/'audio.wav'])
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(OUT/'Opening.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(P['captions']))+'\n',encoding='utf-8')
shutil.copy2(OUT/'Opening.srt',TMP/'captions.srt')
subprocess.run([FF,'-y','-v','error','-i','video.mp4','-i','audio.wav','-vf',"subtitles=captions.srt:force_style='FontName=Arial,FontSize=20,Outline=2,Shadow=0,MarginV=35'",'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','192k','-t','16','-movflags','+faststart',str(OUT/'Opening_Preview.mp4')],cwd=TMP,check=True)
print(OUT/'Opening_Preview.mp4')
