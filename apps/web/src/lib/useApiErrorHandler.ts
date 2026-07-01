"use client";

import { useState, useCallback } from "react";
import { ApiError } from "./api";
import { clearSession } from "./session";

export interface UseApiErrorHandlerReturn {
  accessDenied: boolean;
  accessDeniedMessage: string;
  handleApiError: (error: Error) => void;
  resetAccessDenied: () => void;
}

export function useApiErrorHandler(): UseApiErrorHandlerReturn {
  const [accessDenied, setAccessDenied] = useState(false);
  const [accessDeniedMessage, setAccessDeniedMessage] = useState("");

  const handleApiError = useCallback((error: Error) => {
    if (error instanceof ApiError) {
      if (error.status === 401) {
        clearSession();
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      } else if (error.status === 403) {
        setAccessDenied(true);
        setAccessDeniedMessage(error.message);
      }
    }
  }, []);

  const resetAccessDenied = useCallback(() => {
    setAccessDenied(false);
    setAccessDeniedMessage("");
  }, []);

  return {
    accessDenied,
    accessDeniedMessage,
    handleApiError,
    resetAccessDenied,
  };
}
