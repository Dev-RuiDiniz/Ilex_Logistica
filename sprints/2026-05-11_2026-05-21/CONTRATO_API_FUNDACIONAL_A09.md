# Contrato Técnico API Fundacional (A-09)

Base URL: `/api/v1`

## Autenticação

### POST `/auth/login`
- Perfis: público
- Request:
```json
{ "email": "admin@ilex.com", "password": "123456" }
```
- Response 200:
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```
- Response 401: credenciais inválidas.

### POST `/auth/refresh`
- Perfis: público (com refresh válido)
- Request:
```json
{ "refresh_token": "<jwt>" }
```
- Response 200: novo `access_token`.
- Response 401: refresh token inválido/expirado.

## Transportadoras

### GET `/carriers`
- Perfis: `admin`, `logistica`, `gestor`, `auditoria`
- Query opcional: `include_inactive` (bool, default `false`)
- Response 200: lista de transportadoras.

### POST `/carriers`
- Perfis: `admin`, `logistica`, `gestor`
- Request:
```json
{
  "name": "Transportes B",
  "external_code": "TPB",
  "integration_metadata": { "erp": "totvs" }
}
```
- Response 201: objeto criado.
- Response 409: transportadora já existe.
- Response 422: payload inválido.

### PUT `/carriers/{carrier_id}`
- Perfis: `admin`, `logistica`, `gestor`
- Atualiza campos permitidos.
- Response 200, 404, 422.

### POST `/carriers/{carrier_id}/inactivate`
- Perfis: `admin`, `logistica`, `gestor`
- Inativação lógica (`is_active=false`).
- Response 200, 404.

## Padrão de erro de validação

Para payload inválido (422):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "payload invalido",
    "details": []
  }
}
```
