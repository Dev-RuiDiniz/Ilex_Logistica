"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { useAuth } from "@/features/auth/auth-provider";

export default function PrivateLayout({ children }: { children: React.ReactNode }) {
  const { session } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || !session) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-sm text-gray-400">Carregando...</div>
      </div>
    );
  }

  return <AppShell>{children}</AppShell>;
}
