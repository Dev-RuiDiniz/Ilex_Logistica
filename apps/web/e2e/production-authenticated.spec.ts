import { expect, test } from "@playwright/test";
import { join } from "path";

const enabled = process.env.ILEX_E2E_ALLOW_WRITES === "true";
const email = process.env.ILEX_E2E_EMAIL;
const password = process.env.ILEX_E2E_PASSWORD;

test("smoke autenticado com importação e cotação em homologação", async ({ page }) => {
  test.skip(!enabled || !email || !password, "requer homologação e credenciais E2E descartáveis");
  await page.goto("/login");
  await page.getByLabel(/e-?mail/i).fill(email!);
  await page.getByLabel(/senha/i).fill(password!);
  await page.getByRole("button", { name: /entrar/i }).click();
  await expect(page).toHaveURL(/\/$/);

  await page.goto("/orders");
  const fixture = join(process.cwd(), "..", "api", "tests", "fixtures", "orders", "orders_10.csv");
  await page.getByLabel("Arquivo CSV ou XLSX").setInputFiles(fixture);
  await page.getByRole("button", { name: "Gerar preview" }).click();
  await expect(page.getByText(/10 válidos/)).toBeVisible();
  await page.getByRole("button", { name: "Confirmar importação" }).click();
  const orderLink = page.locator("a:visible", { hasText: "PED-10-00001" }).first();
  await orderLink.click();
  await page.getByRole("button", { name: "Nova rodada" }).click();
  await page.getByRole("link", { name: /Rodada/ }).first().click();
  const firstQuote = page.getByRole("article").first();
  await firstQuote.getByLabel("Valor").fill("100.00");
  await firstQuote.getByLabel("Prazo (dias)").fill("2");
  await firstQuote.getByRole("button", { name: "Salvar" }).click();
  await expect(firstQuote.getByText("Recomendada")).toBeVisible();
});
