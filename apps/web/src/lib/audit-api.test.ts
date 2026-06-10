/* eslint-disable @typescript-eslint/no-explicit-any */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { getAuditLogs, getAuditLogById, getAuditSummary } from "./audit-api";
import * as apiModule from "./api";

// Mock the request function from api module
vi.mock("./api", () => ({
  request: vi.fn(),
}));

describe("audit-api", () => {
  const mockToken = "test-token";

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("getAuditLogs", () => {
    it("chama endpoint correto", async () => {
      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        logs: [],
        total: 0,
        page: 1,
        page_size: 100,
      });

      await getAuditLogs(mockToken, {});

      expect(apiModule.request).toHaveBeenCalledWith(
        expect.stringContaining("/audit"),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: `Bearer ${mockToken}`,
          }),
        })
      );
    });

    it("serializa filtros", async () => {
      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        logs: [],
        total: 0,
        page: 1,
        page_size: 100,
      });

      await getAuditLogs(mockToken, {
        event_type: "test_event",
        entity_type: "test_entity",
        severity: "info",
        status: "success",
        page: 2,
        page_size: 50,
      });

      expect(apiModule.request).toHaveBeenCalledWith(
        expect.stringContaining("event_type=test_event&entity_type=test_entity&severity=info&status=success&page=2&page_size=50"),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: `Bearer ${mockToken}`,
          }),
        })
      );
    });

    it("omite filtros vazios", async () => {
      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        logs: [],
        total: 0,
        page: 1,
        page_size: 100,
      });

      await getAuditLogs(mockToken, {});

      expect(apiModule.request).toHaveBeenCalledWith(
        expect.not.stringContaining("event_type="),
        expect.not.stringContaining("entity_type=")
      );
    });

    it("trata erro de API", async () => {
      (apiModule.request as jest.Mock).mockRejectedValueOnce(new Error("API Error"));

      await expect(getAuditLogs(mockToken, {})).rejects.toThrow("API Error");
    });

    it("retorna payload tipado", async () => {
      const mockLogs = [
        {
          id: 1,
          event_type: "test_event",
          entity_type: "test_entity",
          entity_id: 1,
          action: "create",
          actor_user_id: null,
          actor_email: null,
          source: "api",
          severity: "info" as const,
          status: "success" as const,
          message: "Test message",
          before_json: null,
          after_json: null,
          metadata_json: null,
          request_id: null,
          ip_address: null,
          user_agent: null,
          created_at: "2025-01-21T00:00:00Z",
        },
      ];

      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        logs: mockLogs,
        total: 1,
        page: 1,
        page_size: 100,
      });

      const result = await getAuditLogs(mockToken, {});

      expect(result.logs).toEqual(mockLogs);
      expect(result.total).toBe(1);
      expect(result.page).toBe(1);
      expect(result.page_size).toBe(100);
    });
  });

  describe("getAuditLogById", () => {
    it("chama endpoint correto", async () => {
      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        id: 1,
        event_type: "test_event",
        entity_type: "test_entity",
        entity_id: 1,
        action: "create",
        actor_user_id: null,
        actor_email: null,
        source: "api",
        severity: "info" as const,
        status: "success" as const,
        message: "Test message",
        before_json: null,
        after_json: null,
        metadata_json: null,
        request_id: null,
        ip_address: null,
        user_agent: null,
        created_at: "2025-01-21T00:00:00Z",
      });

      await getAuditLogById(mockToken, 1);

      expect(apiModule.request).toHaveBeenCalledWith(
        expect.stringContaining("/audit/1"),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: `Bearer ${mockToken}`,
          }),
        })
      );
    });

    it("trata erro de API", async () => {
      (apiModule.request as any).mockRejectedValueOnce(new Error("Not found"));

      await expect(getAuditLogById(mockToken, 1)).rejects.toThrow("Not found");
    });

    it("retorna payload tipado", async () => {
      const mockLog = {
        id: 1,
        event_type: "test_event",
        entity_type: "test_entity",
        entity_id: 1,
        action: "create",
        actor_user_id: null,
        actor_email: null,
        source: "api",
        severity: "info" as const,
        status: "success" as const,
        message: "Test message",
        before_json: null,
        after_json: null,
        metadata_json: null,
        request_id: null,
        ip_address: null,
        user_agent: null,
        created_at: "2025-01-21T00:00:00Z",
      };

      (apiModule.request as any).mockResolvedValueOnce(mockLog);

      const result = await getAuditLogById(mockToken, 1);

      expect(result).toEqual(mockLog);
    });
  });

  describe("getAuditSummary", () => {
    it("chama endpoint correto", async () => {
      (apiModule.request as jest.Mock).mockResolvedValueOnce({
        total_logs: 100,
        success_count: 80,
        failed_count: 15,
        skipped_count: 5,
        critical_count: 5,
        warning_count: 10,
        info_count: 85,
        create_count: 50,
        update_count: 30,
        delete_count: 10,
        read_count: 10,
      });

      await getAuditSummary(mockToken);

      expect(apiModule.request).toHaveBeenCalledWith(
        expect.stringContaining("/audit/summary"),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: `Bearer ${mockToken}`,
          }),
        })
      );
    });

    it("trata erro de API", async () => {
      (apiModule.request as any).mockRejectedValueOnce(new Error("API Error"));

      await expect(getAuditSummary(mockToken)).rejects.toThrow("API Error");
    });

    it("retorna payload tipado", async () => {
      const mockSummary = {
        total_logs: 100,
        success_count: 80,
        failed_count: 15,
        skipped_count: 5,
        critical_count: 5,
        warning_count: 10,
        info_count: 85,
        create_count: 50,
        update_count: 30,
        delete_count: 10,
        read_count: 10,
      };

      (apiModule.request as any).mockResolvedValueOnce(mockSummary);

      const result = await getAuditSummary(mockToken);

      expect(result).toEqual(mockSummary);
    });
  });
});
