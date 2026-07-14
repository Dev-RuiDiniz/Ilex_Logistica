# Global Text Legibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Melhorar contraste e legibilidade textual em todo o frontend.

**Architecture:** A mudança começa no design system compartilhado para corrigir a hierarquia base de texto. Depois, as telas e componentes legados que ainda usam classes dispersas de `gray/slate` recebem normalização pontual, mantendo a semântica visual já existente.

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, Vitest

---

### Task 1: Reforçar a escala textual do design system

**Files:**
- Modify: `apps/web/src/app/globals.css`

- [ ] **Step 1: Ajustar tokens e classes base**

Reforçar `--muted`, `page-kicker`, `page-subtitle`, `section-subtitle`, `metric-card-label` e `metric-card-note`.

- [ ] **Step 2: Preservar consistência com a base clara**

Melhorar contraste sem voltar para blocos pesados ou tons escuros excessivos.

### Task 2: Normalizar telas e componentes legados

**Files:**
- Modify: `apps/web/src/app/login/page.tsx`
- Modify: `apps/web/src/components/AccessDenied.tsx`
- Modify: `apps/web/src/components/AuditJsonViewer.tsx`
- Modify: `apps/web/src/components/app-shell.tsx`
- Modify: `apps/web/src/components/SlaBadge.tsx`
- Modify: `apps/web/src/app/(private)/layout.tsx`
- Modify: `apps/web/src/app/(private)/alerts/page.tsx`
- Modify: `apps/web/src/app/(private)/audit/page.tsx`
- Modify: `apps/web/src/app/(private)/carriers/page.tsx`
- Modify: `apps/web/src/app/(private)/dashboard/page.tsx`
- Modify: `apps/web/src/app/(private)/exceptions/page.tsx`
- Modify: `apps/web/src/app/(private)/page.tsx`
- Modify: `apps/web/src/app/(private)/reports/daily/page.tsx`
- Modify: `apps/web/src/app/(private)/settings/sla/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/import/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/deliveries/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/analytics/exceptions/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/DateRangePicker.tsx`

- [ ] **Step 1: Substituir textos fracos**

Trocar `text-gray-500/600/700` e `text-slate-500/600` por tons mais legíveis, mantendo a semântica de cada tela.

- [ ] **Step 2: Revisar conteúdo tabular e estados**

Melhorar leitura de vazios, loading, cabeçalhos de tabela, mensagens auxiliares e detalhes.

### Task 3: Validar a entrega

**Files:**
- Test: `apps/web`

- [ ] **Step 1: Rodar testes**

Run: `cd apps/web && npm test`
Expected: suíte passando

- [ ] **Step 2: Rodar build**

Run: `cd apps/web && npm run build`
Expected: build passando
