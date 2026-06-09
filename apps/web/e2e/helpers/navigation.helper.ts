import { Page, expect } from '@playwright/test';

/**
 * Helper para navegação em testes E2E
 */

export class NavigationHelper {
  constructor(private page: Page) {}

  /**
   * Navega para uma rota específica
   */
  async goTo(route: string) {
    await this.page.goto(route);
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Navega para o dashboard
   */
  async goToDashboard() {
    await this.goTo('/');
    await expect(this.page).toHaveURL('/');
  }

  /**
   * Navega para listagem de shipments
   */
  async goToShipments() {
    await this.goTo('/shipments');
    await expect(this.page).toHaveURL('/shipments');
  }

  /**
   * Navega para importação
   */
  async goToImport() {
    await this.goTo('/shipments/import');
    await expect(this.page).toHaveURL('/shipments/import');
  }

  /**
   * Navega para listagem de deliveries
   */
  async goToDeliveries() {
    await this.goTo('/shipments/deliveries');
    await expect(this.page).toHaveURL('/shipments/deliveries');
  }

  /**
   * Navega para painel de exceções
   */
  async goToExceptions() {
    await this.goTo('/exceptions');
    await expect(this.page).toHaveURL('/exceptions');
  }

  /**
   * Navega para gestão de transportadoras
   */
  async goToCarriers() {
    await this.goTo('/carriers');
    await expect(this.page).toHaveURL('/carriers');
  }

  /**
   * Navega para gestão de usuários
   */
  async goToUsers() {
    await this.goTo('/users');
    await expect(this.page).toHaveURL('/users');
  }

  /**
   * Navega para relatório diário
   */
  async goToDailyReport() {
    await this.goTo('/reports/daily');
    await expect(this.page).toHaveURL('/reports/daily');
  }

  /**
   * Clica em um link de navegação pelo texto
   */
  async clickNavLink(text: string) {
    await this.page.getByRole('link', { name: text }).click();
  }

  /**
   * Verifica se item de menu está visível
   */
  async isMenuItemVisible(text: string): Promise<boolean> {
    const menuItem = this.page.getByRole('link', { name: text });
    return await menuItem.isVisible();
  }

  /**
   * Verifica se item de menu está oculto
   */
  async isMenuItemHidden(text: string): Promise<boolean> {
    const menuItem = this.page.getByRole('link', { name: text });
    const isVisible = await menuItem.isVisible();
    return !isVisible;
  }
}

/**
 * Fixture extendida para navegação
 */
export const navigationHelperFixture = async ({ page }: { page: Page }) => {
  return new NavigationHelper(page);
};
