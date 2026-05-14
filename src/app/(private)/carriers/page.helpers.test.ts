import { describe, expect, it } from "vitest";

import {
  filterCarriersByQuery,
  parseIntegrationMetadata,
  removeCarrierById,
  validateCarrierName,
} from "@/app/(private)/carriers/page";
import type { Carrier } from "@/lib/types";

const carriers: Carrier[] = [
  { id: 1, name: "Alpha", external_code: "A", integration_metadata: {}, is_active: true },
  { id: 2, name: "Beta", external_code: "B", integration_metadata: {}, is_active: true },
];

describe("carriers helpers", () => {
  it("filtra por nome sem diferenciar maiusculas", () => {
    expect(filterCarriersByQuery(carriers, "alp")).toEqual([carriers[0]]);
  });

  it("valida nome minimo", () => {
    expect(validateCarrierName("A")).toBe(false);
    expect(validateCarrierName("Alpha")).toBe(true);
  });

  it("faz parse do metadata json", () => {
    expect(parseIntegrationMetadata("{\"source\":\"x\"}")).toEqual({ source: "x" });
  });

  it("remove item inativado da lista", () => {
    expect(removeCarrierById(carriers, 2)).toEqual([carriers[0]]);
  });
});
