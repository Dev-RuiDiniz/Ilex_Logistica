import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { beforeEach, afterEach, describe, it, vi, expect } from "vitest";
import { useAuth } from "@/features/auth/auth-provider";
import { dispatchCharge } from "@/lib/api";
import ChargeDispatchModal from "./ChargeDispatchModal";

vi.mock("@/lib/api");
vi.mock("@/features/auth/auth-provider");
vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ replace: vi.fn() }),
  usePathname: () => "/shipments",
}));

const mockSession = { accessToken: "test-token", role: "admin" as const };

const mockCarriers = [
  { id: 1, name: "Transportadora A", whatsapp: "+5511999999999", is_active: true, integration_metadata: {} },
  { id: 2, name: "Transportadora B", whatsapp: null, is_active: true, integration_metadata: {} },
];

beforeEach(() => {
  vi.mocked(useAuth).mockReturnValue({ session: mockSession } as never);
  vi.mocked(dispatchCharge).mockResolvedValue({
    enviadas: 1,
    puladas_sem_whatsapp: 1,
    falhas: 0,
    critico_escalonado: 0,
  });
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("ChargeDispatchModal", () => {
  it("abre o modal e exibe filtros", () => {
    render(<ChargeDispatchModal carriers={mockCarriers} onClose={() => {}} />);
    expect(screen.getByText("Disparar cobrança")).toBeInTheDocument();
    expect(screen.getByText("Transportadora")).toBeInTheDocument();
    expect(screen.getByText("UF destino")).toBeInTheDocument();
  });

  it("dispara cobrança e mostra resumo", async () => {
    render(<ChargeDispatchModal carriers={mockCarriers} onClose={() => {}} />);
    fireEvent.click(screen.getByText("Disparar"));
    await waitFor(() => {
      expect(dispatchCharge).toHaveBeenCalledTimes(1);
    });
    expect(dispatchCharge).toHaveBeenCalledWith("test-token", {
      carrier_id: null,
      destination_uf: null,
      dias_min: 1,
      dias_max: 999,
    });
    await waitFor(() => {
      expect(screen.getByText("Enviadas: 1")).toBeInTheDocument();
    });
  });

  it("passa carrier_id quando pré-selecionado", async () => {
    render(<ChargeDispatchModal carriers={mockCarriers} defaultCarrierId={2} onClose={() => {}} />);
    fireEvent.click(screen.getByText("Disparar"));
    await waitFor(() => {
      expect(dispatchCharge).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ carrier_id: 2 }),
      );
    });
  });

  it("trata erro 403 exibindo mensagem", async () => {
    vi.mocked(dispatchCharge).mockRejectedValueOnce(new Error("Acesso negado (403)"));
    render(<ChargeDispatchModal carriers={mockCarriers} onClose={() => {}} />);
    fireEvent.click(screen.getByText("Disparar"));
    await waitFor(() => {
      expect(screen.getByText("Acesso negado (403)")).toBeInTheDocument();
    });
  });
});
