# Manual de treinamento

## Administrador

Gerenciar usuários/perfis e transportadoras; validar configurações sem registrar secrets; acompanhar auditoria e readiness. Exercício: criar usuário descartável, atribuir perfil e confirmar bloqueios.

## Logística

Importar envios/pedidos somente após preview, tratar erros por linha, abrir exceções e registrar tratativas. Em cotações, registrar falha individual em vez de inventar preço. Exercício: pedido → rodada → Web/CSV → histórico.

## Gestor

Usar a mesma janela de filtros em KPIs/ranking/listagem, conferir população válida e justificar override. Exercício: comparar duas cotações empatadas e explicar o desempate.

## Auditoria

Consultar imports, tratativas, alertas, relatórios, rodadas e overrides sem alterar estado. Exercício: localizar autoria e timestamp de uma escolha manual.

## Regras comuns

- Nunca compartilhar senha/token nem anexar planilha/dump integral a chamados.
- Dado ausente não equivale a zero; confirmar período/timezone.
- Em erro, registrar request ID, horário, tela, esperado/real e evidência sanitizada.
- Ações financeiras ou de seleção manual exigem revisão da consequência e justificativa.
