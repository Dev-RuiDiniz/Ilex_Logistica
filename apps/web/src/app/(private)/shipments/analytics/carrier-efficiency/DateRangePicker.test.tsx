import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import { DateRangePicker } from "./DateRangePicker";

describe("DateRangePicker", () => {
  const mockOnChange = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    mockOnChange.mockClear();
  });

  it("Deve renderizar label e inputs", () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    expect(screen.getByLabelText("Período")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Data inicial")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Data final")).toBeInTheDocument();
  });

  it("Deve chamar onChange ao selecionar data inicial (onChange imediato)", async () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    const fromInput = screen.getByPlaceholderText("Data inicial");
    act(() => {
      fireEvent.change(fromInput, { target: { value: "2025-01-15" } });
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledWith({ from: "2025-01-15" });
    });
  });

  it("Deve chamar onChange ao selecionar data final (onChange imediato)", async () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    const toInput = screen.getByPlaceholderText("Data final");
    act(() => {
      fireEvent.change(toInput, { target: { value: "2025-01-31" } });
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledWith({ to: "2025-01-31" });
    });
  });

  it("Deve chamar onChange com ambas as datas (chamado duas vezes, uma para cada input)", async () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    const fromInput = screen.getByPlaceholderText("Data inicial");
    const toInput = screen.getByPlaceholderText("Data final");

    act(() => {
      fireEvent.change(fromInput, { target: { value: "2025-01-15" } });
      fireEvent.change(toInput, { target: { value: "2025-01-31" } });
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledTimes(2);
    });

    // Primeira chamada: apenas from
    expect(mockOnChange).toHaveBeenNthCalledWith(1, { from: "2025-01-15" });
    // Segunda chamada: from + to
    expect(mockOnChange).toHaveBeenNthCalledWith(2, { from: "2025-01-15", to: "2025-01-31" });
  });

  it("Deve limpar data quando input é vazio", async () => {
    render(<DateRangePicker label="Período" value={{ from: "2025-01-15", to: "2025-01-31" }} onChange={mockOnChange} />);

    const fromInput = screen.getByPlaceholderText("Data inicial");
    act(() => {
      fireEvent.change(fromInput, { target: { value: "" } });
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledWith({ to: "2025-01-31", from: undefined });
    });
  });

  it("Deve renderizar botão limpar quando há datas selecionadas", () => {
    render(<DateRangePicker label="Período" value={{ from: "2025-01-15" }} onChange={mockOnChange} />);

    expect(screen.getByText("Limpar datas")).toBeInTheDocument();
  });

  it("Deve chamar onChange com objeto vazio ao clicar limpar", async () => {
    render(<DateRangePicker label="Período" value={{ from: "2025-01-15", to: "2025-01-31" }} onChange={mockOnChange} />);

    act(() => {
      fireEvent.click(screen.getByText("Limpar datas"));
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledWith({});
    });
  });

  it("Não deve renderizar botão limpar quando não há datas", () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    expect(screen.queryByText("Limpar datas")).not.toBeInTheDocument();
  });

  it("Deve aceitar placeholders customizados", () => {
    render(
      <DateRangePicker
        label="Período"
        value={{}}
        onChange={mockOnChange}
        placeholder={{ from: "Início", to: "Fim" }}
      />
    );

    expect(screen.getByPlaceholderText("Início")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Fim")).toBeInTheDocument();
  });

  it("Deve definir min no input de data final baseado na data inicial", async () => {
    render(<DateRangePicker label="Período" value={{ from: "2025-01-15" }} onChange={mockOnChange} />);

    const toInput = screen.getByPlaceholderText("Data final");
    expect(toInput).toHaveAttribute("min", "2025-01-15");
  });

  it("Deve definir max no input de data inicial baseado na data final", async () => {
    render(<DateRangePicker label="Período" value={{ to: "2025-01-31" }} onChange={mockOnChange} />);

    const fromInput = screen.getByPlaceholderText("Data inicial");
    expect(fromInput).toHaveAttribute("max", "2025-01-31");
  });

  it("Não deve chamar onChange com data inválida (formato errado)", async () => {
    render(<DateRangePicker label="Período" value={{}} onChange={mockOnChange} />);

    const fromInput = screen.getByPlaceholderText("Data inicial");
    act(() => {
      fireEvent.change(fromInput, { target: { value: "invalid-date" } });
    });

    await waitFor(() => {
      expect(mockOnChange).not.toHaveBeenCalled();
    });
  });

  it("Deve manter valor existente ao atualizar apenas uma data", async () => {
    render(<DateRangePicker label="Período" value={{ from: "2025-01-15" }} onChange={mockOnChange} />);

    const toInput = screen.getByPlaceholderText("Data final");
    act(() => {
      fireEvent.change(toInput, { target: { value: "2025-01-31" } });
    });

    await waitFor(() => {
      expect(mockOnChange).toHaveBeenCalledWith({ from: "2025-01-15", to: "2025-01-31" });
    });
  });
});