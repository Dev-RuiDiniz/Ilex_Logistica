import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/users';
import { testShipments } from './fixtures/test-data';

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

  // ===========================================================================
  // P1.2 — Cenários adicionais: filtros combinados, URL/estado, ordenação
  // ===========================================================================

  test('deve aplicar filtros combinados (status + UF + cliente)', async ({ page }) => {
    await navHelper.goToShipments();

    // Selecionar status
    const statusSelect = page.locator('select').first();
    await statusSelect.selectOption('pending');

    // Preencher cliente
    const customerInput = page.getByPlaceholder(/cliente/i);
    if (await customerInput.isVisible()) {
      await customerInput.fill('Cliente');
    }

    // Aplicar filtros
    const applyButton = page.getByRole('button', { name: /aplicar/i });
    if (await applyButton.isVisible()) {
      await applyButton.click();
      await page.waitForTimeout(1000);
    }

    // Verificar que a URL contém status=pending
    await expect(page).toHaveURL(/status=pending/);
  });

  test('deve persistir filtros na URL ao recarregar', async ({ page }) => {
    await navHelper.goToShipments();

    // Aplicar filtro de status
    const statusSelect = page.locator('select').first();
    await statusSelect.selectOption('pending');

    // Aplicar filtros
    const applyButton = page.getByRole('button', { name: /aplicar/i });
    if (await applyButton.isVisible()) {
      await applyButton.click();
      await page.waitForTimeout(1000);
    }

    // Verificar URL contém status=pending
    await expect(page).toHaveURL(/status=pending/);

    // Recarregar página
    await page.reload();

    // Verificar que o filtro foi restaurado da URL
    const statusSelectAfter = page.locator('select').first();
    await expect(statusSelectAfter).toHaveValue('pending');
  });

  test('deve limpar filtros e remover query params da URL', async ({ page }) => {
    await navHelper.goToShipments();

    // Aplicar filtro de status
    const statusSelect = page.locator('select').first();
    await statusSelect.selectOption('pending');

    const applyButton = page.getByRole('button', { name: /aplicar/i });
    if (await applyButton.isVisible()) {
      await applyButton.click();
      await page.waitForTimeout(1000);
    }

    // Verificar URL tem query params
    await expect(page).toHaveURL(/status=pending/);

    // Limpar filtros
    const clearButton = page.getByRole('button', { name: /limpar/i });
    await clearButton.click();
    await page.waitForTimeout(500);

    // Verificar URL não tem query params
    await expect(page).toHaveURL(/\/shipments$/);
  });

  test('deve ordenar por coluna diferente do padrão', async ({ page }) => {
    await navHelper.goToShipments();

    // Alterar ordenação
    const sortSelect = page.locator('select').nth(1);
    if (await sortSelect.isVisible()) {
      await sortSelect.selectOption('estimated_delivery');

      // Aplicar filtros para sincronizar URL
      const applyButton = page.getByRole('button', { name: /aplicar/i });
      if (await applyButton.isVisible()) {
        await applyButton.click();
        await page.waitForTimeout(1000);
      }

      // Verificar URL contém sort_by=estimated_delivery
      await expect(page).toHaveURL(/sort_by=estimated_delivery/);
    }
  });

  test('deve paginar e refletir page na URL', async ({ page }) => {
    await navHelper.goToShipments();

    // Verificar se botão Próxima está disponível
    const nextButton = page.getByRole('button', { name: /próxima/i });
    if (await nextButton.isVisible() && await nextButton.isEnabled()) {
      await nextButton.click();
      await page.waitForTimeout(1000);

      // Verificar URL contém page=2
      await expect(page).toHaveURL(/page=2/);
    }
  });

  test('deve buscar com termo inexistente e mostrar estado vazio', async ({ page }) => {
    await navHelper.goToShipments();

    // Preencher busca com termo inexistente
    const searchInput = page.getByPlaceholder(/buscar|pesquisar/i);
    await searchInput.fill('ZZZINEXISTENTE123');

    // Submeter busca
    const searchButton = page.getByRole('button', { name: /buscar/i });
    if (await searchButton.isVisible()) {
      await searchButton.click();
    } else {
      await searchInput.press('Enter');
    }

    await page.waitForTimeout(1000);

    // Verificar estado vazio
    await expect(page.getByText(/nenhum envio encontrado/i)).toBeVisible();
  });
});
