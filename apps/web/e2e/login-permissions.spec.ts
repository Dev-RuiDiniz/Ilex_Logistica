import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/users';

/**
 * Testes E2E: Login e Permissões
 * 
 * Cobre:
 * - Acesso à tela de login
 * - Login como administrador fake
 * - Validação de acesso a rotas por perfil
 * - Login como perfil logística fake
 * - Login como gestor fake
 * - Bloqueio/redirect de rota privada sem sessão
 * - Validação de menu/telas por perfil
 */

test.describe('Login e Permissões', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
  });

  test('deve acessar tela de login', async ({ page }) => {
    await authHelper.goToLogin();
    
    // Verificar URL
    await expect(page).toHaveURL('/login');
    
    // Verificar elementos do formulário
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/senha/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /entrar|login/i })).toBeVisible();
  });

  test('deve logar como administrador fake', async ({ page }) => {
    const adminUser = testUsers.admin;
    
    // Login
    await authHelper.loginAs(adminUser);
    
    // Verificar redirecionamento para dashboard
    await expect(page).toHaveURL('/');
    
    // Verificar que está autenticado
    const isAuthenticated = await authHelper.isAuthenticated();
    expect(isAuthenticated).toBe(true);
  });

  test('deve logar como perfil logística fake', async ({ page }) => {
    const logisticaUser = testUsers.logistica;
    
    // Login
    await authHelper.loginAs(logisticaUser);
    
    // Verificar redirecionamento para dashboard
    await expect(page).toHaveURL('/');
    
    // Verificar que está autenticado
    const isAuthenticated = await authHelper.isAuthenticated();
    expect(isAuthenticated).toBe(true);
  });

  test('deve logar como gestor fake', async ({ page }) => {
    const gestorUser = testUsers.gestor;
    
    // Login
    await authHelper.loginAs(gestorUser);
    
    // Verificar redirecionamento para dashboard
    await expect(page).toHaveURL('/');
    
    // Verificar que está autenticado
    const isAuthenticated = await authHelper.isAuthenticated();
    expect(isAuthenticated).toBe(true);
  });

  test('deve bloquear rota privada sem sessão', async ({ page }) => {
    // Tentar acessar rota privada sem login
    await authHelper.verifyPrivateRouteBlocked('/shipments');
    
    // Verificar redirecionamento para login
    await expect(page).toHaveURL('/login');
  });

  test('admin deve ter acesso a todas as rotas', async () => {
    const adminUser = testUsers.admin;
    
    // Login
    await authHelper.loginAs(adminUser);
    
    // Verificar acesso a rotas esperadas
    for (const route of adminUser.expectedAccessibleRoutes) {
      const canAccess = await authHelper.canAccessRoute(route);
      expect(canAccess, `Admin should access ${route}`).toBe(true);
    }
  });

  test('logística não deve ter acesso a gestão de usuários', async () => {
    const logisticaUser = testUsers.logistica;
    
    // Login
    await authHelper.loginAs(logisticaUser);
    
    // Tentar acessar rota proibida
    const canAccessUsers = await authHelper.canAccessRoute('/users');
    expect(canAccessUsers).toBe(false);
  });

  test('gestor não deve ter acesso a importação', async () => {
    const gestorUser = testUsers.gestor;
    
    // Login
    await authHelper.loginAs(gestorUser);
    
    // Tentar acessar rota proibida
    const canAccessImport = await authHelper.canAccessRoute('/shipments/import');
    expect(canAccessImport).toBe(false);
  });

  test('auditoria deve ter acesso limitado', async () => {
    const auditoriaUser = testUsers.auditoria;
    
    // Login
    await authHelper.loginAs(auditoriaUser);
    
    // Verificar acesso a rotas permitidas
    for (const route of auditoriaUser.expectedAccessibleRoutes) {
      const canAccess = await authHelper.canAccessRoute(route);
      expect(canAccess, `Auditoria should access ${route}`).toBe(true);
    }
    
    // Verificar bloqueio de rotas proibidas
    for (const route of auditoriaUser.expectedForbiddenRoutes) {
      const canAccess = await authHelper.canAccessRoute(route);
      expect(canAccess, `Auditoria should NOT access ${route}`).toBe(false);
    }
  });

  test('menu deve respeitar perfil do usuário', async () => {
    const logisticaUser = testUsers.logistica;
    
    // Login
    await authHelper.loginAs(logisticaUser);
    
    // Verificar itens de menu visíveis
    await expect(navHelper.isMenuItemVisible('Shipments')).toBeTruthy();
    await expect(navHelper.isMenuItemVisible('Importações')).toBeTruthy();
    await expect(navHelper.isMenuItemVisible('Exceções')).toBeTruthy();
    
    // Verificar itens de menu ocultos
    await expect(navHelper.isMenuItemHidden('Usuários')).toBeTruthy();
  });
});
