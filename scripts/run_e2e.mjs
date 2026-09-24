import { spawn } from 'node:child_process';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const port = process.env.PHB_TEST_PORT || '4177';
const server = spawn(process.execPath, [path.join(root, 'scripts', 'serve_static.mjs'), port], {
  cwd: root,
  stdio: 'ignore',
  windowsHide: true,
});

const delay = milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));
async function waitForServer() {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    if (server.exitCode !== null) throw new Error(`Le serveur local s'est arrêté avec le code ${server.exitCode}`);
    try {
      const response = await fetch(`http://127.0.0.1:${port}/`);
      if (response.ok) return;
    } catch {}
    await delay(100);
  }
  throw new Error(`Le serveur local n'a pas répondu sur le port ${port}`);
}

let exitCode = 1;
try {
  await waitForServer();
  const runner = spawn(process.execPath, [path.join(root, 'node_modules', '@playwright', 'test', 'cli.js'), 'test', ...process.argv.slice(2)], {
    cwd: root,
    env: { ...process.env, PHB_EXTERNAL_SERVER: '1', PHB_TEST_PORT: port },
    stdio: 'inherit',
    windowsHide: true,
  });
  exitCode = await new Promise((resolve, reject) => {
    runner.once('error', reject);
    runner.once('exit', code => resolve(code ?? 1));
  });
} finally {
  server.kill();
  await Promise.race([new Promise(resolve => server.once('exit', resolve)), delay(2000)]);
  if (server.exitCode === null) server.kill('SIGKILL');
}
process.exitCode = exitCode;
