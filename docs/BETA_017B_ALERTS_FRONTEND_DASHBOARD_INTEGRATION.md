# BETA-017B: Alerts Frontend and Dashboard Integration

## Overview
Implementation of the frontend for the alerts and notifications system, including visual integration with the dashboard Beta.

> Update 2026-06-17: the implementation is now complete on `feature/beta-027-alerts-notifications`; the frontend also includes the `no_update` filter and the updated alert contract. See `docs/BETA_027_ALERTS_NOTIFICATIONS_COMPLETE.md`.

## Implementation Details

### 1. API Client and Types (`apps/web/src/lib/alerts-api.ts`)
- **Functions implemented:**
  - `getAlerts(filters)`: Fetch alerts with optional filtering
  - `getAlertsSummary()`: Fetch alerts summary statistics
  - `generateAlerts()`: Trigger alert generation
  - `markAlertAsRead(alertId)`: Mark an alert as read
  - `resolveAlert(alertId)`: Resolve an alert

- **TypeScript Types:**
  - `AlertItem`: Alert data structure
  - `AlertsFilters`: Filter parameters for alerts
  - `AlertsSummary`: Summary statistics
  - `AlertsResponse`: API response for alerts list
  - `AlertsSummaryResponse`: API response for summary
  - `GenerateAlertsResponse`: API response for generation
  - `AlertActionResponse`: API response for actions

- **Features:**
  - Automatic token authentication from localStorage
  - Boolean serialization for filter parameters (is_read, is_resolved)
  - Error handling for non-OK responses

### 2. Alerts Page (`apps/web/src/app/(private)/alerts/page.tsx`)
- **Features:**
  - Summary cards displaying key metrics (Total, Active, Unread, Resolved, Critical, Warnings)
  - Filter panel with multiple filter options:
    - Status (active, read, resolved)
    - Severity (critical, warning, info)
    - Type (sla_critical, sla_late, sla_warning, unknown_sla)
    - Read status (is_read)
    - Resolved status (is_resolved)
  - Action buttons:
    - Generate Alerts button
    - Mark as Read button (per alert)
    - Resolve button (per alert)
  - Alerts table displaying:
    - Severity badge
    - Title
    - Message
    - Type
    - Status
    - Read status
    - Resolved status
    - Generated date
    - Actions

- **State Management:**
  - alerts: List of alerts
  - summary: Summary statistics
  - loading: Loading state
  - error: Error state
  - filters: Current filter values

### 3. Dashboard Integration (`apps/web/src/app/(private)/dashboard/page.tsx`)
- **Changes:**
  - Updated "Alertas Ativos" card to display actual count from API
  - Changed display from "0 (módulo não habilitado)" to "Nenhum alerta ativo" when count is 0
  - Added "Ver alertas →" link to alerts page when count > 0
  - Link navigates to `/alerts` route

### 4. Testing

#### API Client Tests (`apps/web/src/lib/alerts-api.test.ts`)
- **Test coverage:** 9 tests
- **Tests:**
  - getAlerts calls correct endpoint
  - getAlerts with query parameters
  - getAlerts serializes boolean is_read
  - getAlerts serializes boolean is_resolved
  - getAlertsSummary calls correct endpoint
  - generateAlerts calls POST endpoint
  - markAlertAsRead calls PATCH endpoint
  - resolveAlert calls PATCH endpoint
  - Error handling for non-OK responses

#### Alerts Page Tests (`apps/web/src/app/(private)/alerts/alerts-page.test.tsx`)
- **Test coverage:** 10 tests
- **Tests:**
  - Renders loading state
  - Renders empty state
  - Renders summary cards
  - Renders alerts list/table
  - Displays critical alert
  - Displays warning alert
  - Renders filters
  - Changes severity filter and refetches
  - Changes alert_type filter and refetches
  - Changes status filter and refetches

#### Dashboard Tests (`apps/web/src/app/(private)/dashboard/dashboard-page.test.tsx`)
- **New tests:**
  - Displays "Nenhum alerta ativo" when count is 0
  - Displays actual count and link to alerts page when count > 0

## Verification

### Frontend Tests
- **Total test files:** 25
- **Total tests:** 226
- **All tests passing:** ✅

### Lint
- **Errors:** 0
- **Warnings:** 6 (pre-existing, unrelated to this implementation)
- **Status:** ✅

### Build
- **TypeScript:** ✅
- **Static generation:** ✅
- **Route `/alerts` included:** ✅
- **Status:** ✅

## Files Created/Modified

### Created
- `apps/web/src/lib/alerts-api.ts` - API client and types
- `apps/web/src/lib/alerts-api.test.ts` - API client tests
- `apps/web/src/app/(private)/alerts/page.tsx` - Alerts page component
- `apps/web/src/app/(private)/alerts/alerts-page.test.tsx` - Alerts page tests

### Modified
- `apps/web/src/app/(private)/dashboard/page.tsx` - Updated alerts card with link
- `apps/web/src/app/(private)/dashboard/dashboard-page.test.tsx` - Added tests for alerts integration

## Integration Points

### Backend API Contract
The frontend uses the following backend endpoints (implemented in BETA-017A):
- `GET /api/v1/alerts` - List alerts with filters
- `GET /api/v1/alerts/summary` - Get summary statistics
- `POST /api/v1/alerts/generate` - Generate alerts
- `PATCH /api/v1/alerts/{id}/read` - Mark as read
- `PATCH /api/v1/alerts/{id}/resolve` - Resolve alert

### Navigation
- Dashboard → Alerts page via "Ver alertas →" link
- Alerts page → Dashboard via navigation menu (existing)

## Next Steps
- [ ] Consider adding real-time updates for alerts (WebSocket/SSE)
- [ ] Add alert notifications/toasts in the UI
- [ ] Implement alert preferences/settings
- [ ] Add alert history/archival functionality
