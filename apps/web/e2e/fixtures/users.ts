/**
 * Fixtures de usuários fake para testes E2E
 * 
 * NOTA: Estes são usuários de teste FAKE com credenciais falsas.
 * NUNCA usar credenciais reais em testes E2E.
 */

export interface TestUser {
  email: string;
  password: string;
  fullName: string;
  roles: string[];
  expectedAccessibleRoutes: string[];
  expectedForbiddenRoutes: string[];
}

export const testUsers: Record<string, TestUser> = {
  admin: {
    email: 'admin-e2e-fake@ilex.test',
    password: 'FakePassword123!',
    fullName: 'Admin E2E Test',
    roles: ['admin'],
    expectedAccessibleRoutes: [
      '/',
      '/shipments',
      '/shipments/import',
      '/shipments/analytics/carrier-efficiency',
      '/shipments/analytics/exceptions',
      '/exceptions',
      '/carriers',
      '/users',
      '/alerts',
      '/audit',
      '/reports/daily',
      '/settings/sla',
    ],
    expectedForbiddenRoutes: [],
  },
  logistica: {
    email: 'logistica-e2e-fake@ilex.test',
    password: 'FakePassword123!',
    fullName: 'Logística E2E Test',
    roles: ['logistica'],
    expectedAccessibleRoutes: [
      '/',
      '/shipments',
      '/shipments/import',
      '/shipments/analytics/carrier-efficiency',
      '/shipments/analytics/exceptions',
      '/exceptions',
      '/carriers',
      '/alerts',
      '/reports/daily',
      '/settings/sla',
    ],
    expectedForbiddenRoutes: ['/users', '/audit'],
  },
  gestor: {
    email: 'gestor-e2e-fake@ilex.test',
    password: 'FakePassword123!',
    fullName: 'Gestor E2E Test',
    roles: ['gestor'],
    expectedAccessibleRoutes: [
      '/',
      '/shipments',
      '/shipments/analytics/carrier-efficiency',
      '/shipments/analytics/exceptions',
      '/exceptions',
      '/carriers',
      '/alerts',
      '/reports/daily',
      '/settings/sla',
    ],
    expectedForbiddenRoutes: ['/shipments/import', '/users', '/audit'],
  },
  auditoria: {
    email: 'auditoria-e2e-fake@ilex.test',
    password: 'FakePassword123!',
    fullName: 'Auditoria E2E Test',
    roles: ['auditoria'],
    expectedAccessibleRoutes: [
      '/',
      '/shipments',
      '/exceptions',
      '/reports/daily',
      '/audit',
    ],
    expectedForbiddenRoutes: [
      '/shipments/import',
      '/shipments/analytics/carrier-efficiency',
      '/shipments/analytics/exceptions',
      '/carriers',
      '/users',
      '/alerts',
      '/settings/sla',
    ],
  },
};

export const defaultUser = testUsers.admin;
