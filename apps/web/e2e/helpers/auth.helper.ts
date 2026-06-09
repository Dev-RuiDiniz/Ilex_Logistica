import { Page, expect } from '@playwright/test';
import { TestUser } from '../fixtures/users';

/**
 * Helper para autenticação em testes E2E
 * 
 * Estratégia:
 * - Usa localStorage para simular sessão autenticada
 * - Não depende de backend real para autenticação
 * - Usa usuários fake com credenciais falsas
 */

export class AuthHelper {
  constructor(private page: Page) {}

  /**
   * Navega para a página de login
   */
  async goToLogin() {
    await this.page.goto('/login');
    await expect(this.page).toHaveURL('/login');
  }

  /**
   * Preenche o formulário de login
   */
  async fillLoginForm(email: string, password: string) {
    await this.page.getByLabel(/email/i).fill(email);
    await this.page.getByLabel(/senha/i).fill(password);
  }

  /**
   * Submete o formulário de login
   */
  async submitLogin() {
    await this.page.getByRole('button', { name: /entrar|login/i }).click();
  }

  /**
   * Login completo com usuário fake
   * 
   * NOTA: Este método simula o login usando localStorage
   * para não depender de backend real em testes E2E.
   */
  async loginAs(user: TestUser) {
    // Navegar para login
    await this.goToLogin();

    // Preencher formulário
    await this.fillLoginForm(user.email, user.password);

    // Submeter
    await this.submitLogin();

    // Aguardar redirecionamento para dashboard
    await expect(this.page).toHaveURL('/');
  }

  /**
   * Simula sessão autenticada via localStorage
   * 
   * Este método é usado quando não queremos depender do fluxo de login real
   * (por exemplo, quando o backend não está disponível).
   */
  async simulateAuthenticatedSession(user: TestUser) {
    await this.page.goto('/');
    
    // Simular token JWT fake no localStorage
    await this.page.evaluate((userData) => {
      localStorage.setItem('access_token', 'fake-jwt-token-for-e2e-tests');
      localStorage.setItem('user', JSON.stringify({
        id: 999,
        email: userData.email,
        full_name: userData.fullName,
        roles: userData.roles,
      }));
    }, user);

    // Recarregar página para aplicar sessão
    await this.page.reload();
  }

  /**
   * Verifica se usuário está autenticado
   */
  async isAuthenticated(): Promise<boolean> {
    const accessToken = await this.page.evaluate(() => {
      return localStorage.getItem('access_token');
    });
    return accessToken !== null;
  }

  /**
   * Logout
   */
  async logout() {
    await this.page.evaluate(() => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    });
    await this.page.goto('/login');
  }

  /**
   * Verifica acesso a rota privada
   */
  async canAccessRoute(route: string): Promise<boolean> {
    await this.page.goto(route);
    const currentUrl = this.page.url();
    
    // Se foi redirecionado para login, não tem acesso
    if (currentUrl.includes('/login')) {
      return false;
    }
    
    // Se tem erro 403 ou similar, não tem acesso
    const hasError = await this.page.getByText(/acesso negado|não autorizado|403/i).isVisible();
    return !hasError;
  }

  /**
   * Verifica bloqueio de rota privada sem sessão
   */
  async verifyPrivateRouteBlocked(route: string) {
    // Garantir logout
    await this.logout();
    
    // Tentar acessar rota privada
    await this.page.goto(route);
    
    // Verificar redirecionamento para login
    await expect(this.page).toHaveURL('/login');
  }
}

/**
 * Fixture extendida para autenticação
 */
export const authHelperFixture = async ({ page }: { page: Page }) => {
  return new AuthHelper(page);
};
