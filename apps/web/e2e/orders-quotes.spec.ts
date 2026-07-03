import { expect, test } from "@playwright/test";

import { AuthHelper } from "./helpers/auth.helper";
import { testUsers } from "./fixtures/users";

const order = {
  id: 1, source: "erp", external_number: "PED-E2E-1", order_date: "2026-07-03",
  customer_name: "Cliente E2E", origin_zip: "01310100", origin_uf: "SP",
  destination_zip: "20040002", destination_uf: "RJ", weight_kg: "10.500",
  volume_count: 2, goods_value: "1200.00", currency: "BRL", status: "active",
  import_history_id: 5, created_by: 1, created_at: "2026-07-03T10:00:00Z", updated_at: "2026-07-03T10:00:00Z",
};
const carriers = [
  { id: 1, name: "Rápida", external_code: "RAP", integration_metadata: {}, is_active: true },
  { id: 2, name: "Segura", external_code: "SEG", integration_metadata: {}, is_active: true },
];

test("pedido CSV → preview → confirmação → rodada → Web/CSV → override → histórico", async ({ page }) => {
  let imported = false;
  let rounds: Record<string, unknown>[] = [];
  let quoteRound = {
    id: 10, order_id: 1, sequence: 1, status: "open", expires_at: "2026-07-04T10:00:00Z",
    recommended_quote_id: null as number | null, selected_quote_id: null as number | null,
    selection_mode: null as string | null, selection_reason: null as string | null,
    quotes: [
      { id: 101, carrier_id: 1, amount: null as string | null, transit_days: null as number | null, status: "pending", message: null, source: "web", valid_until: "2026-07-04T10:00:00Z" },
      { id: 102, carrier_id: 2, amount: null as string | null, transit_days: null as number | null, status: "pending", message: null, source: "web", valid_until: "2026-07-04T10:00:00Z" },
    ],
  };

  await page.route("**/api/v1/**", async (route) => {
    const request = route.request();
    const url = new URL(request.url());
    const path = url.pathname.replace("/api/v1", "");
    const json = (body: unknown, status = 200) => route.fulfill({ status, contentType: "application/json", body: JSON.stringify(body) });
    if (path === "/orders/imports/preview") return json({ import_id: 5, filename: "orders.csv", file_hash: "a".repeat(64), total_rows: 1, valid_rows: 1, invalid_rows: 0, duplicate_rows: 0, preview_items: [], errors: [], warnings: [] });
    if (path === "/orders/imports/confirm") { imported = true; return json({ id: 5, imported_count: 1, rejected_count: 0, status: "CONFIRMED" }); }
    if (path === "/orders" && request.method() === "GET") return json({ items: imported ? [order] : [], total: imported ? 1 : 0, page: 1, page_size: 20 });
    if (path === "/orders/1" && request.method() === "GET") return json(order);
    if (path === "/orders/1/quote-rounds" && request.method() === "GET") return json(rounds);
    if (path === "/orders/1/quote-rounds" && request.method() === "POST") { rounds = [quoteRound]; return json(quoteRound, 201); }
    if (path === "/carriers") return json(carriers);
    if (path === "/quote-rounds/10" && request.method() === "GET") return json(quoteRound);
    if (path === "/quote-rounds/10/quotes" && request.method() === "POST") {
      const payload = request.postDataJSON(); const quote = quoteRound.quotes.find((item) => item.carrier_id === payload.carrier_id)!;
      Object.assign(quote, { status: payload.status, amount: payload.amount ?? null, transit_days: payload.transit_days ?? null, message: payload.message ?? null });
      quoteRound.recommended_quote_id = quote.id; quoteRound.selected_quote_id = quote.id; quoteRound.selection_mode = "automatic"; return json(quoteRound);
    }
    if (path === "/quote-rounds/10/quotes/import/preview") return json({ import_id: 6, valid_rows: 2, invalid_rows: 0 });
    if (path === "/quote-rounds/10/quotes/import/confirm") {
      quoteRound.quotes[0] = { ...quoteRound.quotes[0], status: "quoted", amount: "90.00", transit_days: 3, source: "csv" };
      quoteRound.quotes[1] = { ...quoteRound.quotes[1], status: "quoted", amount: "100.00", transit_days: 1, source: "csv" };
      quoteRound = { ...quoteRound, status: "completed", recommended_quote_id: 101, selected_quote_id: 101, selection_mode: "automatic" };
      rounds = [quoteRound]; return json(quoteRound);
    }
    if (path === "/quote-rounds/10/select/102") {
      quoteRound = { ...quoteRound, selected_quote_id: 102, selection_mode: "manual", selection_reason: "Prazo crítico aprovado para o piloto" };
      rounds = [quoteRound]; return json(quoteRound);
    }
    return json({ detail: `rota mock não tratada: ${path}` }, 500);
  });

  await new AuthHelper(page).loginAs(testUsers.admin);
  await page.goto("/orders");
  await page.getByLabel("Arquivo CSV ou XLSX").setInputFiles({ name: "orders.csv", mimeType: "text/csv", buffer: Buffer.from("fixture") });
  await page.getByRole("button", { name: "Gerar preview" }).click();
  await expect(page.getByText("1 válidos · 0 inválidos · 0 duplicados")).toBeVisible();
  await page.getByRole("button", { name: "Confirmar importação" }).click();
  const orderLink = page.locator("a:visible", { hasText: "PED-E2E-1" }).first();
  await expect(orderLink).toBeVisible();
  await orderLink.click();
  await page.getByRole("button", { name: "Nova rodada" }).click();
  await page.getByRole("link", { name: /Rodada 1/ }).click();

  const first = page.getByRole("article").filter({ hasText: "Rápida" });
  await first.getByLabel("Valor").fill("95.00");
  await first.getByLabel("Prazo (dias)").fill("2");
  await first.getByRole("button", { name: "Salvar" }).click();
  await expect(first.getByText("Recomendada")).toBeVisible();

  await page.getByLabel("Importar cotações CSV").setInputFiles({ name: "quotes.csv", mimeType: "text/csv", buffer: Buffer.from("fixture") });
  await page.getByRole("button", { name: "Importar", exact: true }).click();
  const second = page.getByRole("article").filter({ hasText: "Segura" });
  await second.getByLabel("Justificativa do override").fill("Prazo crítico aprovado para o piloto");
  await second.getByRole("button", { name: "Selecionar com justificativa" }).click();
  await expect(second.getByText("Selecionada")).toBeVisible();

  await page.getByRole("link", { name: "← Pedido" }).click();
  await expect(page.getByText("Rodada 1")).toBeVisible();
});
