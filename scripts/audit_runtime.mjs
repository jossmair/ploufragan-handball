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
    window.__phbVitals = { cls: 0, lcp: 0, lcpElement: null };
    new PerformanceObserver(list => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) window.__phbVitals.cls += entry.value;
      }
    }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver(list => {
      const entries = list.getEntries();
      if (entries.length) {
        const entry = entries.at(-1);
        const element = entry.element;
        window.__phbVitals.lcp = entry.startTime;
        window.__phbVitals.lcpElement = element ? {
          tag: element.tagName.toLowerCase(),
          id: element.id || null,
          classes: [...element.classList].slice(0, 4),
          url: entry.url ? new URL(entry.url).pathname : null,
        } : null;
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });
  const failed = [];
  page.on('requestfailed', request => {
    // Chromium may abort a still-playing video when the audit closes the page.
    if (request.failure()?.errorText !== 'net::ERR_ABORTED') {
      failed.push(`${request.method()} ${request.url()}`);
    }
  });
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
    const paint = Object.fromEntries(performance.getEntriesByType('paint').map(item => [item.name, item.startTime]));
    const byType = {};
    for (const item of resources) {
      const type = item.initiatorType || 'other';
      byType[type] ??= { requests: 0, encodedBytes: 0, decodedBytes: 0 };
      byType[type].requests += 1;
      byType[type].encodedBytes += Math.round(item.encodedBodySize);
      byType[type].decodedBytes += Math.round(item.decodedBodySize);
    }
    return {
      lcpMs: Math.round(window.__phbVitals.lcp),
      lcpElement: window.__phbVitals.lcpElement,
      cls: Number(window.__phbVitals.cls.toFixed(4)),
      fcpMs: Math.round(paint['first-contentful-paint'] || 0),
      ttfbMs: Math.round(navigation.responseStart),
      domContentLoadedMs: Math.round(navigation.domContentLoadedEventEnd),
      loadMs: Math.round(navigation.loadEventEnd),
      domElements: document.getElementsByTagName('*').length,
      encodedBytes: Math.round(resources.reduce((total, item) => total + item.encodedBodySize, 0)),
      decodedBytes: Math.round(resources.reduce((total, item) => total + item.decodedBodySize, 0)),
      requests: resources.length + 1,
      byType,
      renderBlocking: resources
        .filter(item => item.renderBlockingStatus === 'blocking')
        .map(item => new URL(item.name).pathname),
      inpMs: null,
      inpNote: 'NON MESURÉ : aucune interaction utilisateur représentative dans cet audit de chargement local.',
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
