import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
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
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve abrir detalhe de entrega', async ({ page }) => {
    // Navegar para listagem
    await navHelper.goToShipments();
    
    // Clicar em um shipment
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Verificar redirecionamento para detalhe
    await expect(page).toHaveURL(/\/shipments\/\d+/);
    
    // Verificar informações do shipment
    await expect(page.getByText(testShipments[0].tracking_code)).toBeVisible();
    await expect(page.getByText(testShipments[0].recipient_name)).toBeVisible();
  });

  test('deve exibir timeline de tratativas', async ({ page }) => {
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Verificar seção de tratativas/timeline
    await expect(page.getByRole('heading', { name: /tratativas|timeline|histórico/i })).toBeVisible();
  });

  test('deve exibir formulário para nova tratativa', async ({ page }) => {
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Verificar formulário de tratativa
    await expect(page.getByLabel(/comentário|observação/i)).toBeVisible();
    await expect(page.getByLabel(/status/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /adicionar|registrar/i })).toBeVisible();
  });

  test('deve registrar nova tratativa', async ({ page }) => {
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Preencher formulário
    await page.getByLabel(/comentário|observação/i).fill('Tratativa de teste E2E');
    await page.getByLabel(/status/i).click();
    await page.getByText(/em análise/i).click();
    
    // Submeter
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    
    // Aguardar processamento
    await page.waitForTimeout(1000);
    
    // Verificar mensagem de sucesso
    await expect(page.getByText(/sucesso|registrado/i)).toBeVisible();
  });

  test('deve atualizar timeline sem refresh manual', async ({ page }) => {
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Contar tratativas antes
    const treatmentsBefore = await page.getByTestId('treatment-item').count();
    
    // Adicionar tratativa
    await page.getByLabel(/comentário|observação/i).fill('Tratativa de teste E2E');
    await page.getByLabel(/status/i).click();
    await page.getByText(/em análise/i).click();
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    await page.waitForTimeout(1000);
    
    // Contar tratativas depois (sem refresh)
    const treatmentsAfter = await page.getByTestId('treatment-item').count();
    
    // Verificar que timeline atualizou
    expect(treatmentsAfter).toBeGreaterThan(treatmentsBefore);
  });

  test('deve validar campos obrigatórios', async ({ page }) => {
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Tentar submeter sem preencher
    await page.getByRole('button', { name: /adicionar|registrar/i }).click();
    
    // Verificar mensagem de erro
    await expect(page.getByText(/obrigatório|campo/i)).toBeVisible();
  });

  test('perfil sem permissão não deve registrar tratativa', async ({ page }) => {
    // Login como perfil sem permissão (auditoria)
    await authHelper.loginAs(testUsers.auditoria);
    
    // Navegar para detalhe
    await navHelper.goToShipments();
    await page.getByText(testShipments[0].tracking_code).click();
    
    // Verificar que formulário não está visível
    const formButton = page.getByRole('button', { name: /adicionar|registrar/i });
    await expect(formButton).not.toBeVisible();
  });
});
