# Evidência consolidada P4

Estado: **BLOQUEADO**

| Gate | Estado | Evidência |
|---|---|---|
| Segurança/configuração local | PASSOU | testes automatizados e Compose config |
| PostgreSQL 16 real | BLOQUEADO | Docker engine indisponível na sessão |
| Backup/restore real | BLOQUEADO | requer PostgreSQL/VPS |
| Carga 50 usuários | BLOQUEADO | runner preparado; VPS ausente |
| Observabilidade/alertas ativos | BLOQUEADO | configuração preparada; VPS ausente |
| E2E autenticado externo | BLOQUEADO | cenário preparado; credenciais/URL ausentes |
| Deploy/rollback | BLOQUEADO | scripts preparados; imagens/VPS ausentes |

O marcador `Estado: APROVADO` só pode substituir o estado acima depois que todas as linhas tiverem evidência real revisada.
