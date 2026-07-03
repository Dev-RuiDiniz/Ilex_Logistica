import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import OrdersPage from "./page";

const listOrders = vi.fn();
vi.mock("@/lib/api", () => ({
  listOrders: (...args: unknown[]) => listOrders(...args),
  previewOrderImport: vi.fn(),
  confirmOrderImport: vi.fn(),
}));
vi.mock("@/features/auth/auth-provider", () => ({
  useAuth: () => ({ session: { accessToken: "token", role: "logistica", email: "logistica@example.com" } }),
}));
vi.mock("@/lib/useApiErrorHandler", () => ({
  useApiErrorHandler: () => ({ accessDenied: false, accessDeniedMessage: "", handleApiError: vi.fn() }),
}));

describe("OrdersPage", () => {
  beforeEach(() => {
    listOrders.mockResolvedValue({
      items: [{
        id: 1, source: "erp", external_number: "PED-1", order_date: "2026-07-03",
        customer_name: "Cliente Teste", origin_zip: "01310100", origin_uf: "SP",
        destination_zip: "20040002", destination_uf: "RJ", weight_kg: "10.500",
        volume_count: 2, goods_value: "1200.00", currency: "BRL", status: "active",
        import_history_id: 1, created_by: 1, created_at: "2026-07-03T00:00:00Z",
        updated_at: "2026-07-03T00:00:00Z",
      }],
      total: 1, page: 1, page_size: 20,
    });
  });

  it("renderiza filtros, importação e pedido retornado pela API", async () => {
    render(<OrdersPage />);
    expect(screen.getByRole("heading", { name: "Pedidos e cotações" })).toBeInTheDocument();
    expect(screen.getByLabelText("Arquivo CSV ou XLSX")).toBeInTheDocument();
    await waitFor(() => expect(screen.getAllByText("PED-1").length).toBeGreaterThan(0));
    expect(screen.getAllByText("Cliente Teste").length).toBeGreaterThan(0);
  });
});
