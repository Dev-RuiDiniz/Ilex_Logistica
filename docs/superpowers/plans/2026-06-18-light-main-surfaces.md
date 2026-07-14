# Light Main Surfaces Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clarear as superfícies principais do frontend sem mexer no header e na sidebar.

**Architecture:** A mudança fica concentrada no design system compartilhado em `apps/web/src/app/globals.css`, com um ajuste local em `apps/web/src/app/login/page.tsx` para remover o bloco escuro mais dominante fora do shell. A lógica de negócio e os contratos permanecem intactos.

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, Vitest

---

### Task 1: Ajustar superfícies compartilhadas

**Files:**
- Modify: `apps/web/src/app/globals.css`

- [ ] **Step 1: Clarear tokens e containers principais**

Atualizar `surface-panel`, `surface-panel-strong`, `surface-muted`, `page-hero`, `metric-card`, `table-shell` e estados compartilhados para bases claras.

- [ ] **Step 2: Preservar contraste e severidade**

Manter diferenciação visual de `danger`, `warning`, `success` e `accent` em `metric-card` sem voltar para fundos pesados.

### Task 2: Ajustar a composição principal do login

**Files:**
- Modify: `apps/web/src/app/login/page.tsx`

- [ ] **Step 1: Clarear o showcase principal**

Trocar o fundo escuro do bloco esquerdo por uma composição clara com acentos suaves e textos em tons escuros.

- [ ] **Step 2: Preservar estrutura e fluxo**

Não alterar submissão, loading, erros ou testes existentes de login.

### Task 3: Validar a entrega

**Files:**
- Test: `apps/web`

- [ ] **Step 1: Rodar testes**

Run: `cd apps/web && npm test`
Expected: suíte passando

- [ ] **Step 2: Rodar build**

Run: `cd apps/web && npm run build`
Expected: build passando
