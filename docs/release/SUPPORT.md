# Plano de suporte e escalonamento

| Severidade | Exemplo | Resposta | Escalonamento |
|---|---|---:|---|
| S1 crítica | indisponibilidade total, perda/corrupção, bypass de acesso | 15 min | técnico + sponsor + operação imediatos |
| S2 alta | import/cotação bloqueados, KPI materialmente incorreto | 30 min | técnico + gestor operacional |
| S3 média | degradação, erro com contorno, alerta isolado | 4 h úteis | suporte → técnico |
| S4 baixa | dúvida, melhoria, problema cosmético | 1 dia útil | backlog de produto |

## Chamado mínimo

Ambiente/tag, perfil, horário/timezone, request ID, passos, esperado/real, impacto e evidência sanitizada. Não enviar senha, token, `.env`, dump ou dados pessoais desnecessários.

## Fluxo

Suporte tria severidade e runbook; operação confirma impacto; técnico diagnostica e decide correção/rollback; sponsor decide continuidade em S1. Toda aceitação de risco registra responsável, mitigação e prazo.

Contatos nominais/canais devem ser preenchidos e aprovados antes do piloto; permanecem **A CONFIRMAR**.
