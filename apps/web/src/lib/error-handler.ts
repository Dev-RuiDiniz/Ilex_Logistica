import { ApiError } from "./api";

export function handleApiError(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 401) {
      // Redirecionar para login
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
      return "Sessão expirada. Redirecionando para login...";
    }
    if (error.status === 403) {
      return "Você não tem permissão para acessar este recurso.";
    }
    return error.message || "Erro na API";
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Erro desconhecido";
}

export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}
