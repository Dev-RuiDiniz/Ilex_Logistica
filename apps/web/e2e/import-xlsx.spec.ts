import { test, expect } from '@playwright/test';
import { join } from 'path';
import { AuthHelper } from './helpers/auth.helper';
import { NavigationHelper } from './helpers/navigation.helper';
import { testUsers, validXLSXFixtureName } from './fixtures/test-data';

test('XLSX percorre upload, preview, confirmação e resultado', async ({ page }) => {
  await new AuthHelper(page).loginAs(testUsers.admin);
  await new NavigationHelper(page).goToImport();
  const fixture = join(__dirname, 'fixtures', validXLSXFixtureName);

  await page.getByLabel(/arquivo|csv/i).setInputFiles(fixture);
  await expect(page.getByText(validXLSXFixtureName)).toBeVisible();
  await expect(page.getByRole('table')).toBeVisible();
  const confirm = page.getByRole('button', { name: /confirmar|importar/i });
  await expect(confirm).toBeEnabled();
  await confirm.click();
  await expect(page.getByText(/concluída|sucesso|importado/i)).toBeVisible();
});
