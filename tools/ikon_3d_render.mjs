// node tools/ikon_3d_render.mjs : render wordpress/ikon-3d/*.svg -> PNG 192x192 transparan (lalu dikonversi ke WebP oleh Python)
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
const dir = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', 'wordpress', 'ikon-3d');
const port = 9300 + Math.floor(Math.random() * 500);
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'ikon-'));
const ch = spawn('google-chrome', ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let tabs; for (let i = 0; i < 40; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(250); } }
const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m.result || m.error); delete pend[m.id]; } };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 192, height: 192, deviceScaleFactor: 1, mobile: false });
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
  const svg = fs.readFileSync(path.join(dir, f), 'utf8').replace('width="96" height="96"', 'width="192" height="192"');
  const html = `<html><body style="margin:0;background:transparent">${svg}</body></html>`;
  await send('Page.navigate', { url: 'data:text/html;base64,' + Buffer.from(html).toString('base64') }); await sleep(400);
  const s = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 192, height: 192, scale: 1 } });
  fs.writeFileSync(path.join(dir, f.replace('.svg', '.png')), Buffer.from(s.data, 'base64'));
}
ws.close(); ch.kill(); console.log('render selesai', dir);
