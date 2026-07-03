import { test, expect } from '@playwright/test';
import { join } from 'path';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { validXLSXFixtureName } from './fixtures/test-data';
import { testUsers } from './fixtures/users';

test('XLSX percorre upload, preview, confirmação e resultado', async ({ page }) => {
  await page.route('**/api/v1/imports/preview', async (route) => route.fulfill({
    json: {
      import_id: 101, source: 'xlsx', total_rows: 1, valid_rows: 1, invalid_rows: 0,
      duplicate_count: 0, duplicate_rows: 0,
      preview_items: [{ row_number: 2, data: { invoice_number: 'NF-E2E-XLSX-001', customer_name: 'Cliente Sanitizado', destination_uf: 'SP', collection_departure_date: '2026-07-03', invoice_value: 1000, freight_value: 100 } }],
      errors: [], warnings: [],
    },
  }));
  await page.route('**/api/v1/imports/confirm', async (route) => route.fulfill({
    json: { import_id: 101, status: 'completed', total_rows: 1, valid_rows: 1, invalid_rows: 0, imported_count: 1, rejected_count: 0, duplicates_count: 0, created_shipments: [101], errors: [] },
  }));
  await new AuthHelper(page).loginAs(testUsers.admin);
  await new NavigationHelper(page).goToImport();
  const fixture = join(__dirname, 'fixtures', validXLSXFixtureName);

  await page.getByLabel(/arquivo|csv/i).setInputFiles(fixture);
  await expect(page.getByText(validXLSXFixtureName)).toBeVisible();
  await page.getByRole('button', { name: /validar arquivo/i }).click();
  await expect(page.getByRole('table')).toBeVisible();
  const confirm = page.getByRole('button', { name: /confirmar|importar/i });
  await expect(confirm).toBeEnabled();
  await confirm.click();
  await expect(page.getByRole('heading', { name: /importação concluída/i })).toBeVisible();
});
