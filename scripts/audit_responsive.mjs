import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const baseURL = process.env.PHB_BASE_URL || 'http://127.0.0.1:4176';
const widths = [375, 390, 430, 768, 1024, 1440, 1920];
const pages = [
  '/', '/equipes.html', '/jeunes.html', '/resultats.html', '/inscriptions.html',
  '/boutique.html', '/blog.html', '/articles/presentation-seniors-masculins-1.html',
  '/partenaires.html', '/contact.html',
];
const screenshotRoot = join('test-results', 'responsive-audit');
const saveScreenshots = process.env.PHB_AUDIT_SCREENSHOTS === '1';

if (saveScreenshots) await mkdir(screenshotRoot, { recursive: true });
const browser = await chromium.launch();
const results = [];

for (const width of widths) {
  const context = await browser.newContext({
    viewport: { width, height: width < 768 ? 844 : 1000 },
    reducedMotion: 'reduce',
  });
  for (const path of pages) {
    const page = await context.newPage();
    const errors = [];
    page.on('console', message => {
      if (message.type() === 'error' && !message.text().startsWith('Failed to load resource:')) errors.push(message.text());
    });
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(new URL(path, baseURL).href, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const audit = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      brokenImages: [...document.images].filter(image => image.currentSrc && image.complete && image.naturalWidth === 0).map(image => image.currentSrc),
      clippedControls: [...document.querySelectorAll('a,button,input,select,textarea')]
        .filter(element => {
          if (element.closest('.sponsor-marquee, .article-carousel-track')) return false;
          const style = getComputedStyle(element);
          if (style.display === 'none' || style.visibility === 'hidden') return false;
          const rect = element.getBoundingClientRect();
          return rect.width > 0 && (rect.left < -1 || rect.right > document.documentElement.clientWidth + 1);
        })
        .map(element => element.outerHTML.slice(0, 160)),
    }));
    const item = { width, path, status: response?.status() || 0, errors, ...audit };
    results.push(item);
    if (saveScreenshots) {
      const name = (path === '/' ? 'home' : path.replace(/^\//, '').replaceAll('/', '__').replace('.html', ''));
      await page.screenshot({ path: join(screenshotRoot, `${width}-${name}.png`), fullPage: true });
    }
    await page.close();
  }
  await context.close();
}

await browser.close();
await mkdir('reports', { recursive: true });
await writeFile(join('reports', 'responsive-audit.json'), `${JSON.stringify(results, null, 2)}\n`, 'utf8');

const failures = results.filter(item => item.status !== 200 || item.h1 !== 1 || item.overflow > 1 || item.brokenImages.length || item.clippedControls.length || item.errors.length);
console.log(`Responsive : ${results.length} combinaisons vérifiées, ${failures.length} anomalie(s).`);
for (const item of failures) console.log(JSON.stringify(item));
process.exitCode = failures.length ? 1 : 0;
