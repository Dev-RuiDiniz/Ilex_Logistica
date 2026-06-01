import { describe, expect, it } from "vitest";

import { isPrivatePath, shouldRedirectToHome, shouldRedirectToLogin } from "./middleware";

describe("middleware route guards", () => {
  it("detecta paths privados", () => {
    expect(isPrivatePath("/")).toBe(true);
    expect(isPrivatePath("/carriers")).toBe(true);
    expect(isPrivatePath("/carriers/1")).toBe(true);
    expect(isPrivatePath("/login")).toBe(false);
  });

  it("define redirecionamento para login quando sem token", () => {
    expect(shouldRedirectToLogin("/carriers", false)).toBe(true);
    expect(shouldRedirectToLogin("/carriers", true)).toBe(false);
  });

  it("define redirecionamento para home quando login com token", () => {
    expect(shouldRedirectToHome("/login", true)).toBe(true);
    expect(shouldRedirectToHome("/login", false)).toBe(false);
  });
});
