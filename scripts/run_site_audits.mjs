import { spawn } from 'node:child_process';
const port = '4180';
const baseURL = `http://127.0.0.1:${port}`;
const server = spawn(process.execPath, ['scripts/serve_static.mjs', port], { stdio: 'ignore', windowsHide: true });
try {
  let ready = false;
  for (let attempt = 0; attempt < 100; attempt++) {
    if (server.exitCode !== null) throw new Error('Audit server stopped unexpectedly.');
    try { ready = (await fetch(baseURL)).ok; } catch {}
    if (ready) break;
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  if (!ready) throw new Error('Audit server did not start.');
  for (const script of ['audit_sitemap.mjs', 'audit_responsive.mjs', 'audit_runtime.mjs']) {
    const child = spawn(process.execPath, [`scripts/${script}`], {
      stdio: 'inherit', windowsHide: true, env: { ...process.env, PHB_BASE_URL: baseURL },
    });
    const code = await new Promise((resolve, reject) => { child.on('error', reject); child.on('exit', resolve); });
    if (code !== 0) throw new Error(`${script} failed with code ${code}.`);
  }
} finally { server.kill(); }
