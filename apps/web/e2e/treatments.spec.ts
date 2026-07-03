import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { testShipments } from './fixtures/test-data';
import { testUsers } from './fixtures/users';

/**
 * Testes E2E: Tratativas
 * 
 * Cobre:
 * - Abrir detalhe de uma entrega
 * - Registrar tratativa
 * - Validar que histórico/timeline atualiza
 * - Validar mensagem de sucesso/erro
 */

test.describe('Tratativas', () => {
  let authHelper: AuthHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    const shipment = { ...testShipments[0], actual_delivery: null, invoice_number: 'NF-E2E-001', invoice_value: 1000, freight_value: 100, customer_name: 'Cliente E2E', destination_uf: 'SP', is_active: true, created_at: '2026-07-03T10:00:00Z', updated_at: '2026-07-03T10:00:00Z' };
    const treatments: Array<Record<string, unknown>> = [];
    await page.route('**/api/v1/shipments?**', async (route) => route.fulfill({ json: { items: [shipment], total: 1, page: 1, page_size: 20, total_pages: 1 } }));
    await page.route('**/api/v1/shipments/1', async (route) => route.fulfill({ json: shipment }));
    await page.route('**/api/v1/shipments/1/treatments', async (route) => {
      if (route.request().method() === 'POST') {
        const treatment = { id: treatments.length + 1, shipment_id: 1, status: 'em_analise', comment: 'Tratativa de teste E2E', created_by: 1, created_at: new Date().toISOString() };
        treatments.push(treatment);
        await route.fulfill({ status: 201, json: treatment });
        return;
      }
      await route.fulfill({ json: treatments });
    });
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve abrir detalhe de entrega', async ({ page }) => {
    // Navegar para listagem
    await page.goto('/shipments/1');
    
    // Verificar redirecionamento para detalhe
    await expect(page).toHaveURL(/\/shipments\/\d+/);
    
    // Verificar informações do shipment
    await expect(page.getByText(testShipments[0].tracking_code)).toBeVisible();
    await expect(page.getByText(testShipments[0].recipient_name)).toBeVisible();
  });

  test('deve exibir timeline de tratativas', async ({ page }) => {
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Verificar seção de tratativas/timeline
    await expect(page.getByRole('heading', { name: /tratativas|timeline|histórico/i })).toBeVisible();
  });

  test('deve exibir formulário para nova tratativa', async ({ page }) => {
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Verificar formulário de tratativa
    await expect(page.getByLabel(/comentário|observação/i)).toBeVisible();
    await expect(page.getByLabel(/status/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /adicionar|registrar/i })).toBeVisible();
  });

  test('deve registrar nova tratativa', async ({ page }) => {
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Preencher formulário
    await page.getByLabel(/comentário|observação/i).fill('Tratativa de teste E2E');
    await page.getByLabel(/status/i).selectOption('em_tratativa');
    
    // Submeter
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    
    // Aguardar processamento
    await page.waitForTimeout(1000);
    
    // Verificar mensagem de sucesso
    await expect(page.getByText(/sucesso|registrado/i)).toBeVisible();
  });

  test('deve atualizar timeline sem refresh manual', async ({ page }) => {
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Contar tratativas antes
    const treatmentsBefore = await page.getByTestId('treatment-item').count();
    
    // Adicionar tratativa
    await page.getByLabel(/comentário|observação/i).fill('Tratativa de teste E2E');
    await page.getByLabel(/status/i).selectOption('em_tratativa');
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    await page.waitForTimeout(1000);
    
    // Contar tratativas depois (sem refresh)
    const treatmentsAfter = await page.getByTestId('treatment-item').count();
    
    // Verificar que timeline atualizou
    expect(treatmentsAfter).toBeGreaterThan(treatmentsBefore);
  });

  test('deve validar campos obrigatórios', async ({ page }) => {
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Tentar submeter sem preencher
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    
    // Verificar mensagem de erro
    await expect(page.getByText(/obrigatório|campo/i)).toBeVisible();
  });

  test('perfil sem permissão não deve registrar tratativa', async ({ page }) => {
    // Login como perfil sem permissão (auditoria)
    await authHelper.loginAs(testUsers.auditoria);
    
    // Navegar para detalhe
    await page.goto('/shipments/1');
    
    // Verificar que formulário não está visível
    const formButton = page.getByRole('button', { name: /adicionar|registrar/i });
    await expect(formButton).not.toBeVisible();
  });
});
