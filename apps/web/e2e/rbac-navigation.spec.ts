import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/users';

/**
 * Testes E2E: Navegação por Permissão (BETA-020E)
 * 
 * Cobre:
 * - Admin deve acessar todas as 18 páginas integradas
 * - Logística não deve acessar users
 * - Gestor não deve acessar shipments/import
 * - Auditoria não deve acessar páginas restritas
 * - Menu condicional por perfil
 * - Redirecionamento 401
 * - Exibição AccessDenied 403
 */

test.describe('Navegação por Permissão (RBAC)', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
  });

  test('admin deve acessar todas as 18 páginas', async ({ page }) => {
    const adminUser = testUsers.admin;
    
    // Login como admin
    await authHelper.loginAs(adminUser);
    
    // Verificar acesso a todas as rotas esperadas
    for (const route of adminUser.expectedAccessibleRoutes) {
      await page.goto(route);
      
      // Verificar que não foi redirecionado para login
      await expect(page).not.toHaveURL('/login');
      
      // Verificar que não exibe AccessDenied
      const accessDenied = page.getByText(/acesso negado|não autorizado|403/i);
      await expect(accessDenied).not.toBeVisible();
      
      // Verificar que a página carregou (não está em loading)
      await expect(page.getByText(/carregando/i)).not.toBeVisible({ timeout: 5000 });
    }
  });

  test('logística não deve acessar users', async ({ page }) => {
    const logisticaUser = testUsers.logistica;
    
    // Login como logística
    await authHelper.loginAs(logisticaUser);
    
    // Tentar acessar rota proibida
    await page.goto('/users');
    
    // Verificar redirecionamento ou AccessDenied
    const currentUrl = page.url();
    
    if (currentUrl.includes('/login')) {
      // Foi redirecionado para login
      await expect(page).toHaveURL('/login');
    } else {
      // Exibe AccessDenied
      const accessDenied = page.getByText(/acesso negado|não autorizado|403/i);
      await expect(accessDenied).toBeVisible();
    }
  });

  test('gestor não deve acessar shipments/import', async ({ page }) => {
    const gestorUser = testUsers.gestor;
    
    // Login como gestor
    await authHelper.loginAs(gestorUser);
    
    // Tentar acessar rota proibida
    await page.goto('/shipments/import');
    
    // Verificar redirecionamento ou AccessDenied
    const currentUrl = page.url();
    
    if (currentUrl.includes('/login')) {
      // Foi redirecionado para login
      await expect(page).toHaveURL('/login');
    } else {
      // Exibe AccessDenied
      const accessDenied = page.getByText(/acesso negado|não autorizado|403/i);
      await expect(accessDenied).toBeVisible();
    }
  });

  test('auditoria não deve acessar páginas restritas', async ({ page }) => {
    const auditoriaUser = testUsers.auditoria;
    
    // Login como auditoria
    await authHelper.loginAs(auditoriaUser);
    
    // Verificar bloqueio de rotas proibidas
    for (const route of auditoriaUser.expectedForbiddenRoutes) {
      await page.goto(route);
      
      // Verificar redirecionamento ou AccessDenied
      const currentUrl = page.url();
      
      if (currentUrl.includes('/login')) {
        // Foi redirecionado para login
        await expect(page).toHaveURL('/login');
      } else {
        // Exibe AccessDenied
        const accessDenied = page.getByText(/acesso negado|não autorizado|403/i);
        await expect(accessDenied).toBeVisible();
      }
    }
  });

  test('menu deve respeitar perfil do usuário', async () => {
    const logisticaUser = testUsers.logistica;
    
    // Login como logística
    await authHelper.loginAs(logisticaUser);
    
    // Verificar itens de menu visíveis
    await expect(navHelper.isMenuItemVisible('Shipments')).toBeTruthy();
    await expect(navHelper.isMenuItemVisible('Importações')).toBeTruthy();
    await expect(navHelper.isMenuItemVisible('Exceções')).toBeTruthy();
    
    // Verificar itens de menu ocultos
    await expect(navHelper.isMenuItemHidden('Usuários')).toBeTruthy();
  });

  test('deve redirecionar para login ao receber 401', async ({ page }) => {
    const adminUser = testUsers.admin;
    
    // Login como admin
    await authHelper.loginAs(adminUser);
    
    // Simular sessão expirada (remover token do localStorage)
    await page.evaluate(() => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    });
    
    // Tentar acessar rota privada
    await page.goto('/shipments');
    
    // Verificar redirecionamento para login
    await expect(page).toHaveURL('/login');
  });

  test('deve exibir AccessDenied ao receber 403', async ({ page }) => {
    const logisticaUser = testUsers.logistica;
    
    // Login como logística
    await authHelper.loginAs(logisticaUser);
    
    // Tentar acessar rota proibida (users)
    await page.goto('/users');
    
    // Verificar exibição do componente AccessDenied
    const accessDenied = page.getByText(/acesso negado|não autorizado/i);
    await expect(accessDenied).toBeVisible();
    
    // Verificar botão de voltar para dashboard
    const backButton = page.getByRole('link', { name: /voltar|dashboard/i });
    await expect(backButton).toBeVisible();
  });
});
