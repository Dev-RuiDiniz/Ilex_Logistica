"use client";

import { createContext, useContext, useMemo, useState } from "react";

import { clearSession, getSession, saveSession } from "@/lib/session";
import type { SessionData } from "@/lib/types";

interface AuthContextValue {
  session: SessionData | null;
  setSession: (value: SessionData) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSessionState] = useState<SessionData | null>(() => {
    if (typeof window === "undefined") return null;
    return getSession();
  });

  const setSession = (value: SessionData) => {
    saveSession(value);
    setSessionState(value);
  };

  const logout = () => {
    clearSession();
    setSessionState(null);
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
