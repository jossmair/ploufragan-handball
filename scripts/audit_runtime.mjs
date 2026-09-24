import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';

const baseURL = process.env.PHB_BASE_URL || 'http://127.0.0.1:4176';
const paths = [
  '/',
  '/blog.html',
  '/boutique.html',
  '/resultats.html',
  '/articles/presentation-seniors-masculins-1.html',
];

const browser = await chromium.launch();
const results = [];
for (const path of paths) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 1,
    isMobile: true,
    hasTouch: true,
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    window.__phbVitals = { cls: 0, lcp: 0 };
    new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) window.__phbVitals.cls += entry.value;
      }
    }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      if (entries.length) window.__phbVitals.lcp = entries.at(-1).startTime;
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });
  const failed = [];
  page.on('requestfailed', request => failed.push(`${request.method()} ${request.url()}`));
  page.on('response', response => {
    if (response.status() >= 400 && new URL(response.url()).origin === new URL(baseURL).origin) {
      failed.push(`${response.status()} ${response.url()}`);
    }
  });
  await page.goto(baseURL + path, { waitUntil: 'load' });
  await page.waitForTimeout(1800);
  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0];
    const resources = performance.getEntriesByType('resource');
    return {
      lcpMs: Math.round(window.__phbVitals.lcp),
      cls: Number(window.__phbVitals.cls.toFixed(4)),
      domContentLoadedMs: Math.round(navigation.domContentLoadedEventEnd),
      loadMs: Math.round(navigation.loadEventEnd),
      encodedBytes: Math.round(resources.reduce((total, item) => total + item.encodedBodySize, 0)),
      decodedBytes: Math.round(resources.reduce((total, item) => total + item.decodedBodySize, 0)),
      requests: resources.length + 1,
      largest: resources
        .map(item => ({ name: new URL(item.name).pathname, bytes: Math.round(item.encodedBodySize) }))
        .sort((a, b) => b.bytes - a.bytes)
        .slice(0, 5),
    };
  });
  results.push({ path, ...metrics, failed });
  await context.close();
}
await browser.close();
await mkdir('reports', { recursive: true });
await writeFile('reports/performance-audit.json', `${JSON.stringify(results, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(results, null, 2));
if (results.some(item => item.failed.length || item.cls > 0.1 || item.lcpMs > 2500)) process.exitCode = 1;
