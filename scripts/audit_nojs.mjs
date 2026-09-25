import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const ownServer = !process.env.PHB_BASE_URL;
const port = process.env.PHB_NOJS_PORT || '4179';
const baseURL = process.env.PHB_BASE_URL || `http://127.0.0.1:${port}`;
const paths = [
  '/', '/club.html', '/equipes.html', '/seniors-masculins-1.html',
  '/entrainements.html', '/resultats.html', '/inscriptions.html', '/blog.html',
  '/articles/presentation-seniors-masculins-1.html', '/partenaires.html',
  '/devenir-partenaire.html', '/boutique.html', '/contact.html',
];

const delay = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
let server;
if (ownServer) {
  server = spawn(process.execPath, [path.join(root, 'scripts', 'serve_static.mjs'), port], {
    cwd: root,
    stdio: 'ignore',
    windowsHide: true,
  });
  for (let attempt = 0; attempt < 50; attempt += 1) {
    try {
      const response = await fetch(baseURL);
      if (response.ok) break;
    } catch {}
    if (attempt === 49) throw new Error(`Le serveur sans-JS n'a pas répondu sur ${baseURL}`);
    await delay(100);
  }
}

try {
  const browser = await chromium.launch();
  const results = [];
  for (const width of [390, 1440]) {
    const context = await browser.newContext({
      javaScriptEnabled: false,
      viewport: { width, height: 900 },
      reducedMotion: 'reduce',
    });
    for (const pagePath of paths) {
      const page = await context.newPage();
      const response = await page.goto(new URL(pagePath, baseURL).href, { waitUntil: 'load' });
      const state = await page.evaluate(() => {
        const navigation = document.querySelector('#navigation');
        const main = document.querySelector('main');
        const style = navigation ? getComputedStyle(navigation) : null;
        return {
          h1: document.querySelectorAll('h1').length,
          mainCharacters: (main?.innerText || '').trim().length,
          navigationLinks: navigation?.querySelectorAll('a').length || 0,
          navigationVisible: Boolean(navigation && style && style.display !== 'none' && navigation.getBoundingClientRect().height > 0),
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        };
      });
      results.push({ path: pagePath, width, status: response?.status() || 0, ...state });
      await page.close();
    }
    await context.close();
  }
  await browser.close();

  await mkdir('reports', { recursive: true });
  await writeFile('reports/nojs-audit.json', `${JSON.stringify(results, null, 2)}\n`, 'utf8');
  const failures = results.filter(item => (
    item.status !== 200 || item.h1 !== 1 || item.mainCharacters < 150 ||
    item.navigationLinks < 8 || !item.navigationVisible || item.overflow > 1
  ));
  console.log(`Sans JavaScript : ${results.length} rendus vérifiés, ${failures.length} anomalie(s).`);
  for (const item of failures) console.log(JSON.stringify(item));
  process.exitCode = failures.length ? 1 : 0;
} finally {
  if (server) {
    server.kill();
    await Promise.race([new Promise(resolve => server.once('exit', resolve)), delay(2000)]);
    if (server.exitCode === null) server.kill('SIGKILL');
  }
}
