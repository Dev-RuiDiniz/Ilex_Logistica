import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { listSlaRules, createSlaRule, updateSlaRule, recalculateSla } from "@/lib/api";
import SlaRulesPage from "./page";
import { useAuth } from "@/features/auth/auth-provider";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

vi.mock("@/lib/api");
vi.mock("@/features/auth/auth-provider");

const mockSession = {
  accessToken: "test-token",
  role: "gestor",
};

describe("SlaRulesPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession });
  });

  it("Deve listar regras SLA", async () => {
    vi.mocked(listSlaRules).mockResolvedValueOnce([
      {
        id: 1,
        transit_days: 3,
        warning_threshold_days: 1,
        critical_delay_days: 2,
        carrier_id: null,
        destination_uf: null,
        is_active: true,
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
    ]);

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByText("Global")).toBeInTheDocument();
      expect(screen.getByText("3")).toBeInTheDocument(); // transit_days
      expect(screen.getByText("1")).toBeInTheDocument(); // warning
      expect(screen.getByText("2")).toBeInTheDocument(); // critical
      expect(screen.getByText("Ativa")).toBeInTheDocument();
    });
  });

  it("Deve exibir estado vazio", async () => {
    vi.mocked(listSlaRules).mockResolvedValueOnce([]);

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhuma regra SLA encontrada.")).toBeInTheDocument();
    });
  });

  it("Deve criar regra válida", async () => {
    vi.mocked(listSlaRules).mockResolvedValue([]);
    vi.mocked(createSlaRule).mockResolvedValueOnce({});

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Prazo (dias)")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByPlaceholderText("Prazo (dias)"), { target: { value: "5" } });
    fireEvent.change(screen.getByPlaceholderText("Aviso (dias)"), { target: { value: "2" } });
    fireEvent.change(screen.getByPlaceholderText("Crítico (dias)"), { target: { value: "3" } });
    fireEvent.click(screen.getByText("Criar"));

    await waitFor(() => {
      expect(vi.mocked(createSlaRule)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          transit_days: 5,
          warning_threshold_days: 2,
          critical_delay_days: 3,
          carrier_id: null,
          destination_uf: null,
          is_active: true,
        })
      );
    });
  });

  it("Deve exibir erro de API ao criar", async () => {
    vi.mocked(listSlaRules).mockResolvedValue([]);
    vi.mocked(createSlaRule).mockRejectedValueOnce(new Error("API Error"));

    render(<SlaRulesPage />);

    fireEvent.change(screen.getByPlaceholderText("Prazo (dias)"), { target: { value: "5" } });
    fireEvent.change(screen.getByPlaceholderText("Aviso (dias)"), { target: { value: "2" } });
    fireEvent.change(screen.getByPlaceholderText("Crítico (dias)"), { target: { value: "3" } });
    fireEvent.click(screen.getByText("Criar"));

    await waitFor(() => {
      expect(screen.getByText(/API Error/i)).toBeInTheDocument();
    });
  });

  it("Deve editar regra (toggle active)", async () => {
    vi.mocked(listSlaRules).mockResolvedValueOnce([
      {
        id: 1,
        transit_days: 3,
        warning_threshold_days: 1,
        critical_delay_days: 2,
        carrier_id: null,
        destination_uf: null,
        is_active: true,
        created_at: "2025-01-01T00:00:00Z",
        updated_at: "2025-01-01T00:00:00Z",
      },
    ]);
    vi.mocked(updateSlaRule).mockResolvedValueOnce({});

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByText("Inativar")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Inativar"));

    await waitFor(() => {
      expect(vi.mocked(updateSlaRule)).toHaveBeenCalledWith(
        "test-token",
        1,
        { is_active: false }
      );
    });
  });

  it("Deve exibir erro de API ao listar", async () => {
    vi.mocked(listSlaRules).mockRejectedValueOnce(new Error("API Error"));

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByText(/API Error/i)).toBeInTheDocument();
    });
  });

  it("Deve exibir loading", async () => {
    vi.mocked(listSlaRules).mockImplementation(() => new Promise(() => {}));

    render(<SlaRulesPage />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("Deve disparar reprocessamento", async () => {
    vi.mocked(listSlaRules).mockResolvedValue([]);
    vi.mocked(recalculateSla).mockResolvedValueOnce({
      processed_count: 100,
      updated_count: 10,
      skipped_count: 85,
      error_count: 5,
    });

    render(<SlaRulesPage />);

    await waitFor(() => {
      expect(screen.getByText("Reprocessar SLA")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Reprocessar SLA"));

    await waitFor(() => {
      expect(screen.getByText("Processados: 100")).toBeInTheDocument();
      expect(screen.getByText("Atualizados: 10")).toBeInTheDocument();
      expect(screen.getByText("Pulados: 85")).toBeInTheDocument();
      expect(screen.getByText("Erros: 5")).toBeInTheDocument();
    });
  });

  it("Deve exibir contadores de reprocessamento", async () => {
    vi.mocked(listSlaRules).mockResolvedValue([]);
    vi.mocked(recalculateSla).mockResolvedValueOnce({
      processed_count: 50,
      updated_count: 5,
      skipped_count: 45,
      error_count: 0,
    });

    render(<SlaRulesPage />);

    fireEvent.click(screen.getByText("Reprocessar SLA"));

    await waitFor(() => {
      expect(screen.getByText("Processados: 50")).toBeInTheDocument();
      expect(screen.getByText("Atualizados: 5")).toBeInTheDocument();
    });
  });

  it("Deve criar regra com carrier_id e destination_uf", async () => {
    vi.mocked(listSlaRules).mockResolvedValue([]);
    vi.mocked(createSlaRule).mockResolvedValueOnce({});

    render(<SlaRulesPage />);

    fireEvent.change(screen.getByPlaceholderText("Prazo (dias)"), { target: { value: "4" } });
    fireEvent.change(screen.getByPlaceholderText("Aviso (dias)"), { target: { value: "1" } });
    fireEvent.change(screen.getByPlaceholderText("Crítico (dias)"), { target: { value: "2" } });
    fireEvent.change(screen.getByPlaceholderText("ID Transportadora (opcional)"), { target: { value: "123" } });
    fireEvent.change(screen.getByPlaceholderText("UF (opcional)"), { target: { value: "SP" } });
    fireEvent.click(screen.getByText("Criar"));

    await waitFor(() => {
      expect(vi.mocked(createSlaRule)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          transit_days: 4,
          warning_threshold_days: 1,
          critical_delay_days: 2,
          carrier_id: 123,
          destination_uf: "SP",
          is_active: true,
        })
      );
    });
  });
});