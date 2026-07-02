/* eslint-disable @typescript-eslint/no-explicit-any */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getAlerts, getAlertsSummary, generateAlerts, markAlertAsRead, resolveAlert } from './alerts-api';

const token = 'test-token';

const expectApiUrl = (path: string) => expect.stringContaining(`http://localhost:8000/api/v1${path}`);

const expectAuthHeaders = () =>
  expect.objectContaining({
    method: expect.any(String),
    headers: expect.objectContaining({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    }),
  });

describe('alerts-api', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal('fetch', vi.fn());
    vi.stubEnv('NEXT_PUBLIC_API_URL', 'http://localhost:8000/api/v1');
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  describe('getAlerts', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts(token, {});

      expect(global.fetch).toHaveBeenCalledWith(
        expectApiUrl('/alerts'),
        expectAuthHeaders()
      );
    });

    it('envia filtros corretamente', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts(token, {
        status: 'active',
        severity: 'critical',
        alert_type: 'sla_critical',
      });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('status=active'),
        expect.any(Object)
      );
    });

    it('omite filtros vazios', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts(token, {});

      const callArgs = (global.fetch as any).mock.calls[0];
      const url = callArgs[0];
      expect(url).not.toContain('status=');
      expect(url).not.toContain('severity=');
    });

    it('serializa boolean is_read/is_resolved corretamente', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts(token, {
        is_read: true,
        is_resolved: false,
      });

      const callArgs = (global.fetch as any).mock.calls[0];
      const url = callArgs[0];
      expect(url).toContain('is_read=true');
      expect(url).toContain('is_resolved=false');
    });

    it('trata erro de API', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: false,
        status: 500,
      });

      await expect(getAlerts(token, {})).rejects.toThrow();
    });
  });

  describe('getAlertsSummary', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({
          total_alerts: 0,
          active_count: 0,
          read_count: 0,
          resolved_count: 0,
          critical_count: 0,
          warning_count: 0,
          info_count: 0,
        }),
      });

      await getAlertsSummary(token);

      expect(global.fetch).toHaveBeenCalledWith(
        expectApiUrl('/alerts/summary'),
        expectAuthHeaders()
      );
    });
  });

  describe('generateAlerts', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({
          success: true,
          processed_count: 0,
          created_count: 0,
          skipped_count: 0,
          resolved_count: 0,
          error_count: 0,
        }),
      });

      await generateAlerts(token);

      expect(global.fetch).toHaveBeenCalledWith(
        expectApiUrl('/alerts/generate'),
        expectAuthHeaders()
      );
    });
  });

  describe('markAlertAsRead', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, message: 'Alert marked as read' }),
      });

      await markAlertAsRead(token, 1);

      expect(global.fetch).toHaveBeenCalledWith(
        expectApiUrl('/alerts/1/read'),
        expectAuthHeaders()
      );
    });
  });

  describe('resolveAlert', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, message: 'Alert marked as resolved' }),
      });

      await resolveAlert(token, 1);

      expect(global.fetch).toHaveBeenCalledWith(
        expectApiUrl('/alerts/1/resolve'),
        expectAuthHeaders()
      );
    });
  });
});
/* eslint-enable @typescript-eslint/no-explicit-any */
