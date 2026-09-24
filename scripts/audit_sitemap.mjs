import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';

const baseURL = process.env.PHB_BASE_URL || 'http://127.0.0.1:4176';
const sitemap = await readFile('sitemap.xml', 'utf8');
const paths = [...sitemap.matchAll(/<loc>https:\/\/ploufragan-handball\.fr(\/[^<]*)?<\/loc>/g)]
  .map(match => match[1] || '/');
const browser = await chromium.launch();
const results = [];

for (const width of [390, 1440]) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
  for (const path of paths) {
    const page = await context.newPage();
    const errors = [];
    page.on('console', message => {
      if (message.type() === 'error' && !message.text().startsWith('Failed to load resource:')) errors.push(message.text());
    });
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(new URL(path, baseURL).href, { waitUntil: 'load' });
    const state = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      title: document.title,
      brokenImages: [...document.images]
        .filter(image => image.currentSrc && image.complete && image.naturalWidth === 0)
        .map(image => image.currentSrc),
    }));
    results.push({ path, width, status: response?.status() || 0, errors, ...state });
    await page.close();
  }
  await context.close();
}
await browser.close();
await writeFile('reports/sitemap-audit.json', `${JSON.stringify(results, null, 2)}\n`, 'utf8');

const failures = results.filter(item => item.status !== 200 || item.h1 !== 1 || item.overflow > 1 || !item.title || item.brokenImages.length || item.errors.length);
console.log(`Sitemap : ${paths.length} pages, ${results.length} rendus, ${failures.length} anomalie(s).`);
for (const item of failures) console.log(JSON.stringify(item));
process.exitCode = failures.length ? 1 : 0;
