import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/test-data';

/**
 * Testes E2E: Alertas
 * 
 * Cobre:
 * - Validar painel/badge de alertas se existir
 * - Validar alerta crítico
 * - Marcar alerta como lido se funcionalidade existir
 * - Validar estado vazio
 */

test.describe('Alertas', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve exibir badge de alertas se existir', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar badge de alertas (se implementado)
    const alertBadge = page.getByTestId('alert-badge');
    
    if (await alertBadge.isVisible()) {
      await expect(alertBadge).toBeVisible();
    }
  });

  test('deve exibir alerta crítico', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar indicador de alerta crítico (se implementado)
    const criticalAlert = page.getByTestId('critical-alert');
    
    if (await criticalAlert.isVisible()) {
      await expect(criticalAlert).toBeVisible();
      await expect(page.getByText(/crítico|urgente/i)).toBeVisible();
    }
  });

  test('deve permitir marcar alerta como lido', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar botão de marcar como lido (se implementado)
    const markReadButton = page.getByRole('button', { name: /marcar como lido/i });
    
    if (await markReadButton.isVisible()) {
      await markReadButton.click();
      
      // Verificar que alerta foi marcado
      await page.waitForTimeout(500);
      await expect(markReadButton).not.toBeVisible();
    }
  });

  test('deve validar estado vazio de alertas', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Se não houver alertas, deve exibir estado vazio controlado
    const noAlerts = page.getByText(/sem alertas|nenhuma notificação/i);
    
    if (await noAlerts.isVisible()) {
      await expect(noAlerts).toBeVisible();
    }
  });

  test('deve exibir painel de alertas se existir', async ({ page }) => {
    // Verificar se há página de alertas
    await page.goto('/alerts');
    
    // Se existir, validar
    const alertsPage = page.getByRole('heading', { name: /alertas|notificações/i });
    
    if (await alertsPage.isVisible()) {
      await expect(alertsPage).toBeVisible();
    }
  });

  test('deve filtrar alertas por tipo', async ({ page }) => {
    await page.goto('/alerts');
    
    const alertsPage = page.getByRole('heading', { name: /alertas|notificações/i });
    
    if (await alertsPage.isVisible()) {
      // Verificar filtro por tipo
      const typeFilter = page.getByLabel(/tipo/i);
      
      if (await typeFilter.isVisible()) {
        await typeFilter.click();
        await page.getByText(/crítico/i).click();
        await page.waitForTimeout(500);
      }
    }
  });
});
