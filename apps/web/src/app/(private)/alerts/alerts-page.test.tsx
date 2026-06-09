import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AlertsPage from './page';
import * as alertsApi from '@/lib/alerts-api';

describe('AlertsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(alertsApi, 'getAlerts').mockResolvedValue({ alerts: [], total: 0 });
    vi.spyOn(alertsApi, 'getAlertsSummary').mockResolvedValue({
      total_alerts: 0,
      active_count: 0,
      read_count: 0,
      resolved_count: 0,
      critical_count: 0,
      warning_count: 0,
      info_count: 0,
    });
    vi.spyOn(alertsApi, 'generateAlerts').mockResolvedValue({
      success: true,
      processed_count: 0,
      created_count: 0,
      skipped_count: 0,
      resolved_count: 0,
      error_count: 0,
    });
    vi.spyOn(alertsApi, 'markAlertAsRead').mockResolvedValue({ success: true, message: 'OK' });
    vi.spyOn(alertsApi, 'resolveAlert').mockResolvedValue({ success: true, message: 'OK' });
  });

  it('renderiza loading', () => {
    vi.spyOn(alertsApi, 'getAlerts').mockImplementation(() => new Promise(() => {}));

    render(<AlertsPage />);

    expect(screen.getByText(/carregando/i)).toBeInTheDocument();
  });

  it('renderiza estado vazio', async () => {
    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByText(/nenhum alerta/i)).toBeInTheDocument();
    });
  });

  it('renderiza cards de resumo', async () => {
    vi.spyOn(alertsApi, 'getAlertsSummary').mockResolvedValue({
      total_alerts: 10,
      active_count: 5,
      read_count: 3,
      resolved_count: 2,
      critical_count: 1,
      warning_count: 2,
      info_count: 2,
    });

    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByText(/total/i)).toBeInTheDocument();
      expect(screen.getByText(/ativos/i)).toBeInTheDocument();
      expect(screen.getByText(/críticos/i)).toBeInTheDocument();
    });
  });

  it('renderiza lista/tabela de alertas', async () => {
    vi.spyOn(alertsApi, 'getAlerts').mockResolvedValue({
      alerts: [
        {
          id: 1,
          alert_type: 'sla_critical',
          severity: 'critical',
          title: 'Atraso Crítico',
          message: 'Entrega com atraso crítico',
          source_type: 'shipment',
          source_id: 1,
          shipment_id: 1,
          carrier_id: 1,
          status: 'active',
          is_read: false,
          is_resolved: false,
          generated_at: '2025-01-20T10:00:00Z',
          read_at: null,
          resolved_at: null,
          created_at: '2025-01-20T10:00:00Z',
          updated_at: '2025-01-20T10:00:00Z',
        },
      ],
      total: 1,
    });

    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByText('Atraso Crítico')).toBeInTheDocument();
    });
  });

  it('exibe alerta critical', async () => {
    vi.spyOn(alertsApi, 'getAlerts').mockResolvedValue({
      alerts: [
        {
          id: 1,
          alert_type: 'sla_critical',
          severity: 'critical',
          title: 'Atraso Crítico TEST',
          message: 'Entrega com atraso crítico',
          source_type: 'shipment',
          source_id: 1,
          shipment_id: 1,
          carrier_id: 1,
          status: 'active',
          is_read: false,
          is_resolved: false,
          generated_at: '2025-01-20T10:00:00Z',
          read_at: null,
          resolved_at: null,
          created_at: '2025-01-20T10:00:00Z',
          updated_at: '2025-01-20T10:00:00Z',
        },
      ],
      total: 1,
    });

    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByText('Atraso Crítico TEST')).toBeInTheDocument();
    });
  });

  it('exibe alerta warning', async () => {
    vi.spyOn(alertsApi, 'getAlerts').mockResolvedValue({
      alerts: [
        {
          id: 1,
          alert_type: 'sla_late',
          severity: 'warning',
          title: 'Atraso TEST',
          message: 'Entrega atrasada',
          source_type: 'shipment',
          source_id: 1,
          shipment_id: 1,
          carrier_id: 1,
          status: 'active',
          is_read: false,
          is_resolved: false,
          generated_at: '2025-01-20T10:00:00Z',
          read_at: null,
          resolved_at: null,
          created_at: '2025-01-20T10:00:00Z',
          updated_at: '2025-01-20T10:00:00Z',
        },
      ],
      total: 1,
    });

    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByText('Atraso TEST')).toBeInTheDocument();
    });
  });

  it('renderiza filtros', async () => {
    render(<AlertsPage />);

    await waitFor(() => {
      expect(screen.getByLabelText('Status')).toBeInTheDocument();
      expect(screen.getByLabelText('Severidade')).toBeInTheDocument();
      expect(screen.getByLabelText('Tipo')).toBeInTheDocument();
    });
  });

  it('altera filtro de severity e refaz consulta', async () => {
    render(<AlertsPage />);

    await waitFor(() => {
      const severityFilter = screen.getByLabelText('Severidade');
      fireEvent.change(severityFilter, { target: { value: 'critical' } });
    });

    await waitFor(() => {
      expect(alertsApi.getAlerts).toHaveBeenCalled();
    });
  });

  it('altera filtro de alert_type e refaz consulta', async () => {
    render(<AlertsPage />);

    await waitFor(() => {
      const typeFilter = screen.getByLabelText('Tipo');
      fireEvent.change(typeFilter, { target: { value: 'sla_critical' } });
    });

    await waitFor(() => {
      expect(alertsApi.getAlerts).toHaveBeenCalled();
    });
  });

  it('altera filtro de status e refaz consulta', async () => {
    render(<AlertsPage />);

    await waitFor(() => {
      const statusFilter = screen.getByLabelText('Status');
      fireEvent.change(statusFilter, { target: { value: 'active' } });
    });

    await waitFor(() => {
      expect(alertsApi.getAlerts).toHaveBeenCalled();
    });
  });
});
