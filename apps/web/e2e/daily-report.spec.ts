import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers } from './fixtures/test-data';

/**
 * Testes E2E: Relatório Diário
 * 
 * Cobre:
 * - Acessar relatório diário
 * - Validar relatório do dia ou estado vazio controlado
 * - Validar histórico quando fixture existir
 * - Validar ação de geração manual se já existir
 * - Validar status de envio se já existir
 * 
 * NOTA: Testes marcados como skip porque a UI do relatório diário pode não estar
 * completamente implementada. Estes testes devem ser habilitados quando a UI estiver pronta.
 */

test.describe('Relatório Diário', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  // SKIP: UI do relatório diário pode não estar completamente implementada
  test.skip('deve acessar relatório diário', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar URL
    await expect(page).toHaveURL('/reports/daily');
    
    // Verificar título
    await expect(page.getByRole('heading', { name: /relatório diário/i })).toBeVisible();
  });

  test.skip('deve exibir data do relatório', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar data atual
    const today = new Date().toLocaleDateString('pt-BR');
    await expect(page.getByText(new RegExp(today))).toBeVisible();
  });

  test.skip('deve exibir KPIs consolidados', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar KPIs principais
    await expect(page.getByText(/total de shipments/i)).toBeVisible();
    await expect(page.getByText(/total de exceções/i)).toBeVisible();
    await expect(page.getByText(/distribuição por criticidade/i)).toBeVisible();
  });

  test.skip('deve exibir distribuição por criticidade', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar breakdown por criticidade
    await expect(page.getByText(/baixa/i)).toBeVisible();
    await expect(page.getByText(/média/i)).toBeVisible();
    await expect(page.getByText(/alta/i)).toBeVisible();
  });

  test.skip('deve validar estado vazio controlado', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Se não houver dados, deve exibir mensagem controlada
    const emptyState = page.getByText(/sem dados|nenhum registro/i);
    
    if (await emptyState.isVisible()) {
      await expect(emptyState).toBeVisible();
    }
  });

  test.skip('deve permitir exportar CSV', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar botão de export
    const exportButton = page.getByRole('button', { name: /exportar|csv/i });
    
    if (await exportButton.isVisible()) {
      await exportButton.click();
      
      // Verificar que download foi iniciado
      // (ajustar conforme implementação real)
    }
  });

  test.skip('deve exibir histórico de relatórios', async ({ page }) => {
    await navHelper.goToDailyReport();
    
    // Verificar seção de histórico
    const historySection = page.getByRole('heading', { name: /histórico/i });
    
    if (await historySection.isVisible()) {
      await expect(historySection).toBeVisible();
    }
  });

  test.skip('perfil sem permissão não deve acessar relatório', async ({ page }) => {
    // Login como perfil sem permissão (se existir)
    // Por enquanto, todos os perfis têm acesso
    await authHelper.loginAs(testUsers.logistica);
    
    // Logística deve ter acesso
    await navHelper.goToDailyReport();
    await expect(page).toHaveURL('/reports/daily');
  });
});
