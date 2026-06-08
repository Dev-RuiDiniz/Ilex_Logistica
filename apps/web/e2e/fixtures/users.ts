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
      '/shipments/deliveries',
      '/exceptions',
      '/carriers',
      '/users',
      '/reports/daily',
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
      '/shipments/deliveries',
      '/exceptions',
      '/carriers',
      '/reports/daily',
    ],
    expectedForbiddenRoutes: ['/users'],
  },
  gestor: {
    email: 'gestor-e2e-fake@ilex.test',
    password: 'FakePassword123!',
    fullName: 'Gestor E2E Test',
    roles: ['gestor'],
    expectedAccessibleRoutes: [
      '/',
      '/shipments',
      '/shipments/deliveries',
      '/exceptions',
      '/carriers',
      '/reports/daily',
    ],
    expectedForbiddenRoutes: ['/shipments/import', '/users'],
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
    ],
    expectedForbiddenRoutes: ['/shipments/import', '/shipments/deliveries', '/carriers', '/users'],
  },
};

export const defaultUser = testUsers.admin;
