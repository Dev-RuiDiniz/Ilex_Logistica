/**
 * Fixtures de dados de teste para E2E
 * 
 * Dados fake para testar fluxos da UI sem depender de backend real.
 */

export interface TestDelivery {
  id: number;
  nf: string;
  transportadora: string;
  data_coleta: string;
  valor_frete: number;
  percentual_frete: number;
}

export interface TestShipment {
  id: number;
  tracking_code: string;
  carrier_id: number;
  carrier_name: string;
  status: string;
  estimated_delivery: string;
  recipient_name: string;
  recipient_phone: string;
  origin_address: string;
  destination_address: string;
  delay_days: number;
  criticality: 'baixa' | 'media' | 'alta';
}

export interface TestCarrier {
  id: number;
  name: string;
  external_code: string;
  is_active: boolean;
}

export const testDeliveries: TestDelivery[] = [
  {
    id: 1,
    nf: 'NF-E2E-001',
    transportadora: 'Transportadora E2E Test',
    data_coleta: '2026-06-08',
    valor_frete: 150.75,
    percentual_frete: 11.0,
  },
  {
    id: 2,
    nf: 'NF-E2E-002',
    transportadora: 'Transportadora E2E Test',
    data_coleta: '2026-06-07',
    valor_frete: 200.50,
    percentual_frete: 12.5,
  },
];

export const testShipments: TestShipment[] = [
  {
    id: 1,
    tracking_code: 'TRACK-E2E-001',
    carrier_id: 1,
    carrier_name: 'Transportadora E2E Test',
    status: 'em_transito',
    estimated_delivery: '2026-06-10',
    recipient_name: 'Destinatário E2E Test',
    recipient_phone: '11999999999',
    origin_address: 'Rua Origem E2E, 123',
    destination_address: 'Rua Destino E2E, 456',
    delay_days: 0,
    criticality: 'baixa',
  },
  {
    id: 2,
    tracking_code: 'TRACK-E2E-002',
    carrier_id: 1,
    carrier_name: 'Transportadora E2E Test',
    status: 'atrasado',
    estimated_delivery: '2026-06-05',
    recipient_name: 'Destinatário E2E Test 2',
    recipient_phone: '11999999998',
    origin_address: 'Rua Origem E2E, 789',
    destination_address: 'Rua Destino E2E, 012',
    delay_days: 3,
    criticality: 'alta',
  },
];

export const testCarriers: TestCarrier[] = [
  {
    id: 1,
    name: 'Transportadora E2E Test',
    external_code: 'CARR-E2E-001',
    is_active: true,
  },
  {
    id: 2,
    name: 'Transportadora E2E Inativa',
    external_code: 'CARR-E2E-002',
    is_active: false,
  },
];

export const validCSVContent = `nf,transportadora,data_coleta,valor_frete,percentual_frete
NF-E2E-001,Transportadora E2E Test,2026-06-08,150.75,11.0
NF-E2E-002,Transportadora E2E Test,2026-06-07,200.50,12.5
NF-E2E-003,Transportadora E2E Test,2026-06-06,180.25,10.5`;

export const invalidCSVContent = `nf,transportadora,data_coleta
NF-E2E-INVALID,Transportadora E2E Test`;

export const validXLSXFixtureName = 'import-valid.xlsx';
