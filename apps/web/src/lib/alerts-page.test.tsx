import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import AlertsPage from '@/app/(private)/alerts/page';
import * as alertsApi from '@/lib/alerts-api';
import { useAuth } from '@/features/auth/auth-provider';

vi.mock('@/features/auth/auth-provider');

const mockSession = {
  accessToken: 'test-token',
  refreshToken: 'refresh-token',
  email: 'admin@ilex.com',
  roles: ['admin'],
};

describe('AlertsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession, setSession: vi.fn(), logout: vi.fn() });
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
});
