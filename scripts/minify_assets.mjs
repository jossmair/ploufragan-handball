import { readFile, writeFile } from 'node:fs/promises';
import { minify } from 'terser';
import CleanCSS from 'clean-css';

// Keep readable sources; publish compact versions of the shared stylesheet and script.
const css = new CleanCSS({ level: 1 }).minify(await readFile('assets/site.css', 'utf8'));
if (css.errors.length) throw new Error(css.errors.join('\n'));
const js = await minify(await readFile('assets/site.js', 'utf8'), { compress: true, mangle: true });
await writeFile('assets/site.min.css', css.styles + '\n');
await writeFile('assets/site.min.js', js.code + '\n');
console.log(`Shared assets: CSS ${Buffer.byteLength(css.styles)} bytes; JS ${Buffer.byteLength(js.code)} bytes.`);
