import { describe, expect, it } from 'vitest';
import {
  filterCarriersByQuery,
  validateCarrierName,
  parseIntegrationMetadata,
  removeCarrierById,
} from './page';
import type { Carrier } from '@/lib/types';

describe('Carriers Page Helpers', () => {
  describe('filterCarriersByQuery', () => {
    it('deve filtrar transportadoras por nome (case insensitive)', () => {
      const carriers: Carrier[] = [
        { id: 1, name: 'Braspress', external_code: 'BRAS', integration_metadata: {}, is_active: true },
        { id: 2, name: 'Jadlog', external_code: 'JADL', integration_metadata: {}, is_active: true },
        { id: 3, name: 'Transit', external_code: 'TRAN', integration_metadata: {}, is_active: true },
      ];

      const result = filterCarriersByQuery(carriers, 'bras');
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Braspress');
    });

    it('deve retornar todas as transportadoras quando query está vazia', () => {
      const carriers: Carrier[] = [
        { id: 1, name: 'Braspress', external_code: 'BRAS', integration_metadata: {}, is_active: true },
        { id: 2, name: 'Jadlog', external_code: 'JADL', integration_metadata: {}, is_active: true },
      ];

      const result = filterCarriersByQuery(carriers, '');
      expect(result).toHaveLength(2);
    });

    it('deve retornar array vazio quando não há correspondência', () => {
      const carriers: Carrier[] = [
        { id: 1, name: 'Braspress', external_code: 'BRAS', integration_metadata: {}, is_active: true },
      ];

      const result = filterCarriersByQuery(carriers, 'xyz');
      expect(result).toHaveLength(0);
    });
  });

  describe('validateCarrierName', () => {
    it('deve validar nome com pelo menos 2 caracteres', () => {
      expect(validateCarrierName('AB')).toBe(true);
      expect(validateCarrierName('Transportadora')).toBe(true);
    });

    it('deve rejeitar nome com menos de 2 caracteres', () => {
      expect(validateCarrierName('A')).toBe(false);
      expect(validateCarrierName('')).toBe(false);
    });

    it('deve rejeitar nome com apenas espaços', () => {
      expect(validateCarrierName('  ')).toBe(false);
    });

    it('deve aceitar nome com espaços no início/fim', () => {
      expect(validateCarrierName('  Transportadora  ')).toBe(true);
    });
  });

  describe('parseIntegrationMetadata', () => {
    it('deve parsear JSON válido', () => {
      const result = parseIntegrationMetadata('{"key": "value"}');
      expect(result).toEqual({ key: 'value' });
    });

    it('deve retornar objeto vazio quando string está vazia', () => {
      const result = parseIntegrationMetadata('');
      expect(result).toEqual({});
    });

    it('deve retornar objeto vazio quando string é null/undefined', () => {
      const result = parseIntegrationMetadata(null as unknown as string);
      expect(result).toEqual({});
    });

    it('deve parsear JSON complexo', () => {
      const result = parseIntegrationMetadata('{"api_key": "123", "enabled": true, "config": {"url": "https://api.example.com"}}');
      expect(result).toEqual({
        api_key: '123',
        enabled: true,
        config: { url: 'https://api.example.com' },
      });
    });
  });

  describe('removeCarrierById', () => {
    it('deve remover transportadora por ID', () => {
      const carriers: Carrier[] = [
        { id: 1, name: 'Braspress', external_code: 'BRAS', integration_metadata: {}, is_active: true },
        { id: 2, name: 'Jadlog', external_code: 'JADL', integration_metadata: {}, is_active: true },
        { id: 3, name: 'Transit', external_code: 'TRAN', integration_metadata: {}, is_active: true },
      ];

      const result = removeCarrierById(carriers, 2);
      expect(result).toHaveLength(2);
      expect(result.find((c) => c.id === 2)).toBeUndefined();
    });

    it('deve retornar array original quando ID não existe', () => {
      const carriers: Carrier[] = [
        { id: 1, name: 'Braspress', external_code: 'BRAS', integration_metadata: {}, is_active: true },
      ];

      const result = removeCarrierById(carriers, 999);
      expect(result).toHaveLength(1);
    });

    it('deve retornar array vazio quando array original está vazio', () => {
      const result = removeCarrierById([], 1);
      expect(result).toHaveLength(0);
    });
  });
});
