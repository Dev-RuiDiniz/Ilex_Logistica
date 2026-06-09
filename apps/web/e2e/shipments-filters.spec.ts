import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers, testShipments } from './fixtures/test-data';

/**
 * Testes E2E: Entregas Monitoradas e Filtros
 * 
 * Cobre:
 * - Abrir listagem de entregas
 * - Validar colunas principais
 * - Aplicar filtros por transportadora, cliente, UF, status/criticidade
 * - Validar limpar filtros
 * - Validar busca global
 */

test.describe('Entregas Monitoradas e Filtros', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve abrir listagem de entregas', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Verificar URL
    await expect(page).toHaveURL('/shipments');
    
    // Verificar título
    await expect(page.getByRole('heading', { name: /shipments|entregas/i })).toBeVisible();
  });

  test('deve exibir colunas principais', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Verificar tabela de shipments
    const table = page.getByRole('table');
    await expect(table).toBeVisible();
    
    // Verificar colunas principais (ajustar conforme implementação real)
    await expect(page.getByText(/rastreio|tracking/i)).toBeVisible();
    await expect(page.getByText(/nf|nota fiscal/i)).toBeVisible();
    await expect(page.getByText(/cliente|destinatário/i)).toBeVisible();
    await expect(page.getByText(/status/i)).toBeVisible();
    await expect(page.getByText(/criticidade/i)).toBeVisible();
  });

  test('deve aplicar filtro por transportadora', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Selecionar transportadora no filtro
    const carrierFilter = page.getByLabel(/transportadora/i);
    await carrierFilter.click();
    await page.getByText(testShipments[0].carrier_name).click();
    
    // Aguardar filtragem
    await page.waitForTimeout(1000);
    
    // Verificar que filtro foi aplicado
    await expect(page.getByText(testShipments[0].carrier_name)).toBeVisible();
  });

  test('deve aplicar filtro por status', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Selecionar status no filtro
    const statusFilter = page.getByLabel(/status/i);
    await statusFilter.click();
    await page.getByText(/em trânsito/i).click();
    
    // Aguardar filtragem
    await page.waitForTimeout(1000);
    
    // Verificar que filtro foi aplicado
    await expect(page.getByText(/em trânsito/i)).toBeVisible();
  });

  test('deve aplicar filtro por criticidade', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Selecionar criticidade no filtro
    const criticalityFilter = page.getByLabel(/criticidade/i);
    await criticalityFilter.click();
    await page.getByText(/alta/i).click();
    
    // Aguardar filtragem
    await page.waitForTimeout(1000);
    
    // Verificar que filtro foi aplicado
    await expect(page.getByText(/alta/i)).toBeVisible();
  });

  test('deve limpar filtros', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Aplicar filtro
    const carrierFilter = page.getByLabel(/transportadora/i);
    await carrierFilter.click();
    await page.getByText(testShipments[0].carrier_name).click();
    await page.waitForTimeout(1000);
    
    // Limpar filtros
    const clearButton = page.getByRole('button', { name: /limpar/i });
    await clearButton.click();
    
    // Aguardar limpeza
    await page.waitForTimeout(1000);
    
    // Verificar que filtros foram limpos
    await expect(page.getByText(/todos/i)).toBeVisible();
  });

  test('deve validar busca global', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Preencher busca global
    const searchInput = page.getByPlaceholder(/buscar|pesquisar/i);
    await searchInput.fill(testShipments[0].tracking_code);
    
    // Aguardar busca
    await page.waitForTimeout(1000);
    
    // Verificar resultado da busca
    await expect(page.getByText(testShipments[0].tracking_code)).toBeVisible();
  });

  test('deve acessar detalhe de shipment', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Clicar em um shipment
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Verificar redirecionamento para detalhe
    await expect(page).toHaveURL(/\/shipments\/\d+/);
    
    // Verificar informações do detalhe
    await expect(page.getByText(testShipments[0].tracking_code)).toBeVisible();
  });

  test('deve validar paginação', async ({ page }) => {
    await navHelper.goToShipments();
    
    // Verificar controles de paginação
    const pagination = page.getByRole('navigation', { name: /paginação/i });
    
    if (await pagination.isVisible()) {
      // Verificar botão próxima página
      const nextPageButton = page.getByRole('button', { name: /próxima|>/i });
      if (await nextPageButton.isEnabled()) {
        await nextPageButton.click();
        await page.waitForTimeout(1000);
      }
    }
  });
});
