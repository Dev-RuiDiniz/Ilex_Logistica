"use client";

import { createContext, useContext, useMemo, useState } from "react";

import { clearSession, saveSession } from "@/lib/session";
import type { SessionData } from "@/lib/types";

interface AuthContextValue {
  session: SessionData | null;
  setSession: (value: SessionData) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const DEV_SESSION: SessionData = {
  email: "dev@ilex.com",
  accessToken: "dev-token-bypass",
  refreshToken: "dev-refresh-bypass",
  role: "admin",
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session] = useState<SessionData>(DEV_SESSION);

  const setSession = (value: SessionData) => {
    saveSession(value);
  };

  const logout = () => {
    clearSession();
  };

  const value = useMemo(() => ({ session, setSession, logout }), [session]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider");
  }
  return ctx;
}
