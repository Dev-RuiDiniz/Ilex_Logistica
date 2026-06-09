import { defineConfig, devices } from '@playwright/test';

/**
 * Configuração do Playwright para testes E2E do Ilex Logística
 * 
 * Estratégia:
 * - Rodar contra ambiente local real (http://localhost:3000)
 * - Usar headless mode por padrão (CI)
 * - Capturar screenshots/traces apenas em falha
 * - Não expor dados sensíveis em artefatos
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    // Não expor dados sensíveis em screenshots
    ignoreHTTPSErrors: true,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // Teste responsivo em viewport menor
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  // Servidor de desenvolvimento para testes
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },

  // Timeout global para testes
  timeout: 30 * 1000,
  expect: {
    timeout: 5 * 1000,
  },
});
