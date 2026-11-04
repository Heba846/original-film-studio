import {Config} from '@remotion/cli/config';
// Cloud session: use the preinstalled headless shell instead of downloading one.
// On another machine, delete this line (or point it at your own Chrome) and Remotion will fetch its own.
if (process.env.OFS_CHROME !== 'download') {
  Config.setBrowserExecutable(process.env.OFS_CHROME || '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell');
}
Config.setVideoImageFormat('jpeg');
