/* eslint-disable @typescript-eslint/no-explicit-any */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getAlerts, getAlertsSummary, generateAlerts, markAlertAsRead, resolveAlert } from './alerts-api';

describe('alerts-api', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  describe('getAlerts', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts({});

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/alerts'),
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('envia filtros corretamente', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ alerts: [], total: 0 }),
      });

      await getAlerts({
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

      await getAlerts({});

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

      await getAlerts({
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

      await expect(getAlerts({})).rejects.toThrow();
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

      await getAlertsSummary();

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/alerts/summary'),
        expect.objectContaining({
          method: 'GET',
        })
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

      await generateAlerts();

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/alerts/generate'),
        expect.objectContaining({
          method: 'POST',
        })
      );
    });
  });

  describe('markAlertAsRead', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, message: 'Alert marked as read' }),
      });

      await markAlertAsRead(1);

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/alerts/1/read'),
        expect.objectContaining({
          method: 'PATCH',
        })
      );
    });
  });

  describe('resolveAlert', () => {
    it('chama endpoint correto', async () => {
      (global.fetch as any).mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, message: 'Alert marked as resolved' }),
      });

      await resolveAlert(1);

      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v1/alerts/1/resolve'),
        expect.objectContaining({
          method: 'PATCH',
        })
      );
    });
  });
});
/* eslint-enable @typescript-eslint/no-explicit-any */
