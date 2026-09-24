import { defineConfig, devices } from '@playwright/test';

const port = process.env.PHB_TEST_PORT || '4177';
const baseURL = `http://127.0.0.1:${port}`;
const externalServer = process.env.PHB_EXTERNAL_SERVER === '1';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  expect: { timeout: 7_000 },
  reporter: [['list']],
  use: {
    baseURL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: externalServer ? undefined : {
    command: `node scripts/serve_static.mjs ${port}`,
    url: baseURL,
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
  projects: [
    { name: 'desktop-chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile-chromium', use: { ...devices['Pixel 7'] } },
  ],
});
