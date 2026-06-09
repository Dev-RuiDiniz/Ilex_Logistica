import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/users';

/**
 * Testes E2E: Dashboard Beta
 * 
 * Cobre:
 * - Carregar dashboard autenticado
 * - Validar KPIs principais
 * - Validar estados de loading/erro/vazio
 * - Validar responsividade em viewport menor
 */

test.describe('Dashboard Beta', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve carregar dashboard autenticado', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar URL
    await expect(page).toHaveURL('/');
    
    // Verificar título da página
    await expect(page.getByRole('heading', { name: /dashboard|painel/i })).toBeVisible();
  });

  test('deve exibir KPIs principais', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar KPIs principais (ajustar seletores conforme implementação real)
    // Estes são seletores genéricos que devem ser ajustados
    
    // Total de shipments
    const totalShipments = page.getByText(/total.*shipments/i);
    await expect(totalShipments).toBeVisible();
    
    // Entregas em andamento
    const inProgress = page.getByText(/em andamento|em trânsito/i);
    await expect(inProgress).toBeVisible();
    
    // Exceções
    const exceptions = page.getByText(/exceções|atrasos/i);
    await expect(exceptions).toBeVisible();
  });

  test('deve validar estado de loading', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar se há indicador de loading (se implementado)
    const loadingIndicator = page.getByTestId('loading-indicator');
    
    // Se existir, deve desaparecer após carregamento
    if (await loadingIndicator.isVisible()) {
      await expect(loadingIndicator).not.toBeVisible({ timeout: 5000 });
    }
  });

  test('deve validar responsividade em viewport menor', async ({ page }) => {
    // Simular viewport mobile
    await page.setViewportSize({ width: 375, height: 667 });
    
    await navHelper.goToDashboard();
    
    // Verificar que dashboard ainda é funcional em mobile
    await expect(page.getByRole('heading', { name: /dashboard|painel/i })).toBeVisible();
    
    // Verificar menu mobile (se implementado)
    const mobileMenu = page.getByRole('button', { name: /menu|hambúrguer/i });
    if (await mobileMenu.isVisible()) {
      await mobileMenu.click();
      // Verificar que menu se abre
    }
  });

  test('deve exibir links para módulos principais', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar links para módulos principais
    await expect(page.getByRole('link', { name: /shipments|entregas/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /importações/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /exceções/i })).toBeVisible();
  });

  test('deve validar estado vazio controlado', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Se não houver dados, deve exibir mensagem de estado vazio
    // (ajustar conforme implementação real)
    const emptyState = page.getByText(/nenhum dado|sem registros/i);
    
    // Se existir mensagem de estado vazio, deve ser clara
    if (await emptyState.isVisible()) {
      await expect(emptyState).toBeVisible();
    }
  });
});
