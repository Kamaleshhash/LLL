# Land Litigation Lookup + Survey-Based Case Tracking (SIH 2025 PS-16 MVP)

Full-stack MVP for linking land records (survey + village) with court litigation records.

## 1) Project Plan

### Phase 1: Foundational MVP (implemented)
- Unified search by `state + district + village_name + survey_number`
- Linked display of RoR-style parcel metadata + ongoing/historical cases
- Case detail view with CNR, court, parties, filing/last/next hearing, stage, status, order URL
- Verification badge with payload hash and source verification logs
- Timeline of case events and GIS polygon visualization
- OTP-based mock login and guest mode
- Alert subscriptions (email/SMS destination stored)
- Filters: case type, status, filing date range
- Natural language query endpoint (semantic heuristic)
- Autocomplete for village spelling variations (fuzzy matching)
- Bulk search endpoint for administrative/institutional users
- Exportable PDF case summary
- Fallbacks for no matches and non-digitized data hints

### Phase 2: Production Connectors (planned)
- Replace mock ingestion with signed API clients for eCourts/NJDG + state RoR portals
- Scheduled ETL jobs, webhook listeners, and immutable verification chain
- Consent and privacy workflows per DPDP Act 2023

### Phase 3: AI + Scale (planned)
- Improved multilingual transliteration, semantic search embeddings
- Risk-scoring model for dispute probability
- Queue-based sync, caching, observability, and horizontal scaling

## 2) Monorepo Structure

```text
backend/
  apps/
    accounts/        OTP auth + roles
    records/         Land/case domain models
    search_api/      search, autocomplete, NLQ, bulk, seed command
    alerts/          alert subscriptions
    analytics/       hotspot analytics
    reports/         PDF generation
  data/              mock JSON feeds (Salem demo included)
  landlitigation/    Django settings/urls
frontend/
  src/
    components/      portal UI modules
    api/             axios client
    i18n/            English/Tamil strings
```

## 3) Backend Setup (local)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_mvp_data
python manage.py runserver
```

API base: `http://127.0.0.1:8000/api`

## 4) Frontend Setup (local)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

UI URL: `http://127.0.0.1:5173`

## 5) Demo Scenario (Salem, TN)

Search with:
- State: `Tamil Nadu`
- District: `Salem`
- Village: `Veerapandi`
- Survey: `45/2B`

Expected: linked pending cases including title dispute + encroachment, verification hash, timeline, polygon map.

## 6) Key API Endpoints

- `POST /api/auth/request-otp/`
- `POST /api/auth/verify-otp/`
- `POST /api/search/`
- `GET /api/search/autocomplete/village/?state=&district=&query=`
- `POST /api/search/nlq/`
- `GET /api/search/cases/<cnr_number>/`
- `POST /api/search/bulk/` (admin/institutional)
- `POST /api/alerts/`
- `GET /api/analytics/hotspots/`
- `GET /api/reports/case-summary/<cnr_number>/`

## 7) Security and Compliance Notes

- Role-aware access control for bulk operations
- Token auth for protected endpoints
- Verification hash per ingested land record
- Designed extension points for signed source payloads and audit logs
- Placeholder for PII masking and consent logging for DPDP compliance workflows

## 8) Accessibility + UX Notes

- Responsive layout for mobile and desktop
- Clear form labels, structured tables, high-contrast government-style palette
- English/Tamil language switch

## 9) MVP Gaps (explicit)

- OTP is mock (no SMS/email gateway yet)
- Real eCourts/state API integrations are stubs
- Risk model is heuristic (not ML-trained yet)
- No production queue/caching yet

