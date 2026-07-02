import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { listShipments } from "@/lib/api";
import ShipmentsPage from "./page";
import { useAuth } from "@/features/auth/auth-provider";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

let mockSearchParams = new URLSearchParams();
const mockReplace = vi.fn();

vi.mock("@/lib/api");
vi.mock("@/features/auth/auth-provider");
vi.mock("next/navigation", () => ({
  useSearchParams: () => mockSearchParams,
  useRouter: () => ({ replace: mockReplace }),
  usePathname: () => "/shipments",
}));

const mockSession = {
  accessToken: "test-token",
  role: "gestor",
};

const emptyResponse = {
  items: [],
  total: 0,
  total_pages: 0,
  page: 1,
  page_size: 20,
};

describe("Shipments URL sync", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession });
    vi.mocked(listShipments).mockResolvedValue(emptyResponse);
    mockSearchParams = new URLSearchParams();
    mockReplace.mockClear();
  });

  it("Deve refletir filtro status na URL apos Aplicar Filtros", async () => {
    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getAllByText("Status").length).toBeGreaterThan(0);
    });

    const statusLabel = screen.getAllByText("Status")[0];
    const statusSelect = statusLabel.closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(statusSelect, { target: { value: "pending" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalled();
      const lastCall = mockReplace.mock.calls[mockReplace.mock.calls.length - 1];
      expect(lastCall[0]).toContain("status=pending");
    });
  });

  it("Deve restaurar filtro da URL no mount inicial", async () => {
    mockSearchParams = new URLSearchParams("status=delivered&customer_name=Cliente%20X");

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ status: "delivered", customer_name: "Cliente X" })
      );
    });
  });

  it("Deve remover query params da URL ao limpar filtros", async () => {
    mockSearchParams = new URLSearchParams("status=pending");

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Limpar")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText("Limpar")).not.toBeDisabled();
    });

    fireEvent.click(screen.getByText("Limpar"));

    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalledWith("/shipments", { scroll: false });
    });
  });

  it("Deve atualizar page na URL ao paginar", async () => {
    vi.mocked(listShipments).mockResolvedValue({
      items: [],
      total: 50,
      total_pages: 3,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Próxima/)).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/Próxima/));

    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalled();
      const lastCall = mockReplace.mock.calls[mockReplace.mock.calls.length - 1];
      expect(lastCall[0]).toContain("page=2");
    });
  });

  it("Deve atualizar sort_by na URL ao ordenar", async () => {
    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Ordenar/)).toBeInTheDocument();
    });

    const sortSelect = screen.getByText(/Ordenar/).closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(sortSelect, { target: { value: "estimated_delivery" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalled();
      const lastCall = mockReplace.mock.calls[mockReplace.mock.calls.length - 1];
      expect(lastCall[0]).toContain("sort_by=estimated_delivery");
    });
  });

  it("Deve lidar com URL com params invalidos sem quebrar", async () => {
    mockSearchParams = new URLSearchParams("page=abc&sort_by=invalid_field");

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum envio encontrado.")).toBeInTheDocument();
    });
  });
});
