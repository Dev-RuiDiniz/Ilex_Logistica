import type { Metadata } from "next";
<<<<<<< HEAD

import { AuthProvider } from "@/features/auth/auth-provider";
import "./globals.css";

=======
import { IBM_Plex_Mono, Manrope } from "next/font/google";
import "./globals.css";

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
});

const plexMono = IBM_Plex_Mono({
  variable: "--font-plex-mono",
  weight: ["400", "500", "600"],
  subsets: ["latin"],
});

>>>>>>> fix/infra-setup-local
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
<<<<<<< HEAD
    <html lang="pt-BR" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <AuthProvider>{children}</AuthProvider>
      </body>
=======
    <html
      lang="pt-BR"
      className={`${manrope.variable} ${plexMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
>>>>>>> fix/infra-setup-local
    </html>
  );
}
