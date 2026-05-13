export type UserRole = "admin" | "logistica" | "gestor" | "auditoria";

export interface SessionData {
  accessToken: string;
  refreshToken: string;
  role: UserRole;
  email: string;
}

export interface Carrier {
  id: number;
  name: string;
  external_code?: string | null;
  integration_metadata: Record<string, unknown>;
  is_active: boolean;
}
