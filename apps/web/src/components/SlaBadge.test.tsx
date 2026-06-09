import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { SlaBadge } from "./SlaBadge";

describe("SlaBadge component", () => {
  it("Deve renderizar badge 'No prazo'", () => {
    render(<SlaBadge status="on_time" />);
    expect(screen.getByText("No prazo")).toBeInTheDocument();
  });

  it("Deve renderizar badge 'Atenção'", () => {
    render(<SlaBadge status="warning" />);
    expect(screen.getByText("Atenção")).toBeInTheDocument();
  });

  it("Deve renderizar badge 'Atrasada'", () => {
    render(<SlaBadge status="late" />);
    expect(screen.getByText("Atrasada")).toBeInTheDocument();
  });

  it("Deve renderizar badge 'Crítica'", () => {
    render(<SlaBadge status="critical" />);
    expect(screen.getByText("Crítica")).toBeInTheDocument();
  });

  it("Deve renderizar 'Sem SLA' quando status unknown", () => {
    render(<SlaBadge status="unknown" />);
    expect(screen.getByText("Sem SLA")).toBeInTheDocument();
  });

  it("Deve renderizar '-' quando status null", () => {
    render(<SlaBadge status={null} />);
    expect(screen.getByText("-")).toBeInTheDocument();
  });
});
