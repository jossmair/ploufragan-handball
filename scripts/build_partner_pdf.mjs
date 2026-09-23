import { chromium } from '@playwright/test';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(pathToFileURL(path.join(root, 'scripts', 'dossier-partenaire-print.html')).href, { waitUntil: 'networkidle' });
await page.pdf({
  path: path.join(root, 'assets', 'dossier-partenaire-phb.pdf'),
  format: 'A4',
  printBackground: true,
  margin: { top: '0', right: '0', bottom: '0', left: '0' },
});
await browser.close();
console.log('Dossier partenaire PDF généré');
