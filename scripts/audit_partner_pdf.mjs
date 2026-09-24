import { chromium } from '@playwright/test';
import { mkdir, readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 1300 } });
await page.emulateMedia({ media: 'print' });
await page.goto(pathToFileURL(path.join(root, 'scripts', 'dossier-partenaire-print.html')).href, { waitUntil: 'networkidle' });
const pages = page.locator('.page');
const count = await pages.count();
if (count !== 4) throw new Error(`Le dossier partenaire doit contenir 4 pages, reçu : ${count}`);
await mkdir(path.join(root, 'test-results', 'partner-kit'), { recursive: true });
for (let index = 0; index < count; index += 1) {
  const item = pages.nth(index);
  const box = await item.boundingBox();
  const overflow = await item.evaluate(element => element.scrollHeight - element.clientHeight);
  if (!box || Math.abs(box.width / box.height - 210 / 297) > 0.01 || overflow > 1) {
    throw new Error(`Mise en page A4 invalide à la page ${index + 1}`);
  }
  await item.screenshot({ path: path.join(root, 'test-results', 'partner-kit', `page-${index + 1}.png`) });
}
await browser.close();

const pdf = await readFile(path.join(root, 'assets', 'dossier-partenaire-phb.pdf'));
const text = pdf.toString('latin1');
const pdfPages = [...text.matchAll(/\/Type\s*\/Page(?!s)/g)].length;
if (pdfPages !== 4 || pdf.length < 50_000) throw new Error(`PDF invalide : ${pdfPages} pages, ${pdf.length} octets`);
console.log(`Dossier partenaire : ${count} pages A4 contrôlées, PDF de ${pdf.length} octets.`);
