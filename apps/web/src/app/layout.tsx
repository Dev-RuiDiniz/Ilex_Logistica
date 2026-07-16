import type { Metadata } from "next";

import { AuthProvider } from "@/features/auth/auth-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ilex Logistica - Web",
  description: "Painel administrativo da Ilex Logistica",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
