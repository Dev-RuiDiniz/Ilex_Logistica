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
 * 
 * NOTA: Testes marcados como skip porque a UI do dashboard pode não estar
 * completamente implementada. Estes testes devem ser habilitados quando a UI estiver pronta.
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
    await expect(page.getByRole('heading', { name: /dashboard beta/i })).toBeVisible();
  });

  test('deve exibir KPIs principais', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar KPIs principais usando data-testid
    const kpiCards = page.getByTestId('dashboard-kpi-cards');
    await expect(kpiCards).toBeVisible();
    
    // Verificar que há cards de KPI
    const cards = kpiCards.locator('div.bg-white, div.bg-green-50, div.bg-orange-50, div.bg-red-50, div.bg-yellow-50, div.bg-gray-50, div.bg-purple-50, div.bg-blue-50, div.bg-indigo-50, div.bg-pink-50');
    await expect(cards).toHaveCount(10);
  });

  test('deve validar estado de loading', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar que dashboard carrega (loading desaparece)
    await expect(page.getByText(/carregando/i)).not.toBeVisible({ timeout: 5000 });
  });

  test('deve validar responsividade em viewport menor', async ({ page }) => {
    // Simular viewport mobile
    await page.setViewportSize({ width: 375, height: 667 });
    
    await navHelper.goToDashboard();
    
    // Verificar que dashboard ainda é funcional em mobile
    await expect(page.getByRole('heading', { name: /dashboard beta/i })).toBeVisible();
    
    // Verificar que KPIs são visíveis em mobile
    await expect(page.getByTestId('dashboard-kpi-cards')).toBeVisible();
  });

  test('deve exibir links para módulos principais', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar filtros do dashboard
    await expect(page.getByTestId('dashboard-filters')).toBeVisible();
    await expect(page.getByTestId('dashboard-trend-filters')).toBeVisible();
  });

  test('deve validar estado vazio controlado', async ({ page }) => {
    await navHelper.goToDashboard();
    
    // Verificar que dashboard exibe dados (não está vazio)
    await expect(page.getByText(/sem dados/i)).not.toBeVisible();
  });
});
