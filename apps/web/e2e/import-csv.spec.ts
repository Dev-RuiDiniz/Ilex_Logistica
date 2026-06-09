import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers, validCSVContent, invalidCSVContent } from './fixtures/test-data';
import { writeFileSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

/**
 * Testes E2E: Importação CSV/XLSX
 * 
 * Cobre:
 * - Acessar tela de importação
 * - Upload de CSV válido
 * - Validar preview
 * - Confirmar importação
 * - Validar mensagem de sucesso
 * - Upload de arquivo inválido
 * - Validar mensagem de erro
 * - Validar bloqueio de botão com erro
 */

test.describe('Importação CSV/XLSX', () => {
  let authHelper: AuthHelper;
  let navHelper: NavigationHelper;

  test.beforeEach(async ({ page }) => {
    authHelper = new AuthHelper(page);
    navHelper = new NavigationHelper(page);
    
    // Login como admin
    await authHelper.loginAs(testUsers.admin);
  });

  test('deve acessar tela de importação', async ({ page }) => {
    await navHelper.goToImport();
    
    // Verificar URL
    await expect(page).toHaveURL('/shipments/import');
    
    // Verificar elementos da tela
    await expect(page.getByRole('heading', { name: /importação/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /upload|selecionar arquivo/i })).toBeVisible();
  });

  test('deve fazer upload de CSV válido', async ({ page }) => {
    await navHelper.goToImport();
    
    // Criar arquivo CSV temporário
    const tempFilePath = join(tmpdir(), 'test-valid.csv');
    writeFileSync(tempFilePath, validCSVContent);
    
    // Fazer upload
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Verificar que arquivo foi carregado
    await expect(page.getByText(/test-valid.csv/i)).toBeVisible();
  });

  test('deve validar preview de importação', async ({ page }) => {
    await navHelper.goToImport();
    
    // Criar arquivo CSV temporário
    const tempFilePath = join(tmpdir(), 'test-preview.csv');
    writeFileSync(tempFilePath, validCSVContent);
    
    // Fazer upload
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Aguardar preview
    await page.waitForTimeout(1000);
    
    // Verificar tabela de preview
    const previewTable = page.getByRole('table');
    await expect(previewTable).toBeVisible();
    
    // Verificar colunas principais
    await expect(page.getByText(/nf/i)).toBeVisible();
    await expect(page.getByText(/transportadora/i)).toBeVisible();
    await expect(page.getByText(/data coleta/i)).toBeVisible();
  });

  test('deve exibir mensagem de erro para arquivo inválido', async ({ page }) => {
    await navHelper.goToImport();
    
    // Criar arquivo CSV inválido temporário
    const tempFilePath = join(tmpdir(), 'test-invalid.csv');
    writeFileSync(tempFilePath, invalidCSVContent);
    
    // Fazer upload
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Aguardar validação
    await page.waitForTimeout(1000);
    
    // Verificar mensagem de erro
    await expect(page.getByText(/erro|inválido|colunas obrigatórias/i)).toBeVisible();
  });

  test('deve bloquear botão de confirmação com erro', async ({ page }) => {
    await navHelper.goToImport();
    
    // Criar arquivo CSV inválido temporário
    const tempFilePath = join(tmpdir(), 'test-block.csv');
    writeFileSync(tempFilePath, invalidCSVContent);
    
    // Fazer upload
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Aguardar validação
    await page.waitForTimeout(1000);
    
    // Verificar que botão de confirmação está desabilitado
    const confirmButton = page.getByRole('button', { name: /confirmar|importar/i });
    await expect(confirmButton).toBeDisabled();
  });

  test('deve exibir mensagem de sucesso após importação', async ({ page }) => {
    await navHelper.goToImport();
    
    // Criar arquivo CSV válido temporário
    const tempFilePath = join(tmpdir(), 'test-success.csv');
    writeFileSync(tempFilePath, validCSVContent);
    
    // Fazer upload
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Aguardar preview
    await page.waitForTimeout(1000);
    
    // Confirmar importação
    const confirmButton = page.getByRole('button', { name: /confirmar|importar/i });
    await confirmButton.click();
    
    // Aguardar processamento
    await page.waitForTimeout(2000);
    
    // Verificar mensagem de sucesso
    await expect(page.getByText(/sucesso|importado com sucesso/i)).toBeVisible();
  });

  test('deve validar formato de arquivo', async ({ page }) => {
    await navHelper.goToImport();
    
    // Tentar上传 arquivo não suportado
    const tempFilePath = join(tmpdir(), 'test.txt');
    writeFileSync(tempFilePath, 'invalid content');
    
    const fileInput = page.getByLabel(/arquivo|csv/i);
    await fileInput.setInputFiles(tempFilePath);
    
    // Verificar mensagem de erro de formato
    await expect(page.getByText(/formato|csv|excel/i)).toBeVisible();
  });
});
