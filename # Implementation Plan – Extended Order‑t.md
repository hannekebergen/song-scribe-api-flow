# Implementation Plan – Extended Order‑types & AI Prompt Flow

> **Project**: JouwSong Dashboard & API
>
> **Objective**: Introduce multi‑type order handling (Standard, Rush, Up‑sell, Order‑bump) with AI‑assisted prompt & lyric generation while maintaining existing UX, accessibility and deployment pipeline.

---

## 1  Context & Rationale

The platform currently treats every Plug\&Pay order as a *new song*. However we now sell:

| Commercial offer               | Internal *OrderType* | Key difference                  |
| ------------------------------ | -------------------- | ------------------------------- |
| Persoonlijk Lied – **72 uur**  | `STANDARD`           | New song; delivery in 3 days    |
| Persoonlijk Lied – **24 uur**  | `RUSH`               | New song; SLA 24 h              |
| **Extra coupletten / Revisie** | `UPSELL`             | Needs original lyrics to extend |
| Karaoke / Instrumental track   | `BUMP`               | No AI; just fulfilment          |

The UI must surface these types and drive different generation flows. Back‑end needs to expose original lyrics for `UPSELL` and respect tighter timeout for `RUSH`.

---

## 2  Scope

* **In**: Dashboard & OrderDetail adjustments, prompt templates, lyric generation & extension endpoints, DB migration for `order_type` & `origin_song_id`.
* **Out**: Studio audio production, payment logic, legacy orders prior to 2024.

---

## 3  Data‑model Changes

Migration via Alembic

```sql
ALTER TABLE orders ADD COLUMN order_type VARCHAR(12) NOT NULL DEFAULT 'STANDARD';
ALTER TABLE orders ADD COLUMN origin_song_id UUID NULL; -- only for UPSELL
CREATE INDEX idx_orders_type ON orders(order_type);
```

Back‑fill script: iterate over existing rows, inspect `products` JSON and set `order_type` accordingly.

---

## 4  Back‑end Work

| Task                                          | Owner | Est. |
| --------------------------------------------- | ----- | ---- |
| `determine_order_type(products[])` helper     | BE    | 2 h  |
| `/orders/{id}/original-lyrics` (GET)          | BE    | 3 h  |
| `/ai/generate` → supports mode `"extend"`     | BE    | 2 h  |
| Update `fetch_orders` to include `order_type` | BE    | 1 h  |
| Celery task deadlines (`eta`) for `RUSH`      | BE    | 1 h  |

*Note*: environment variable names stay unchanged; only payload shape evolves.

---

## 5  Front‑end Work

1. **Dashboard**

   * Insert *Type Order* column.
   * Badge colours: Std = blue‑100, Rush = rose‑500, Up = amber‑400, Bump = gray‑300.
2. **OrderDetail** (conditional rendering)

   * **STANDARD/RUSH**: Prompt card ➜ Songtekst‑editor.
   * **UPSELL**: show readonly existing lyrics + "Extra coupletten" editor.
   * **BUMP**: hide AI panels; only fulfilment checklist.
3. **Prompt Card**

   * Auto‑populate via `/ai/draft‑prompt` hook on first open.
   * Manual edit → `Save` persists to `orders.prompt` column.
4. **State management**: Extend `useFetchOrders` + `Order` TS type.

---

## 6  Prompt Templates

```
/prompts/standard.ts
/prompts/rush.ts        // identical, but include ⏱ deadline
/prompts/upsell.ts      // "Add {n} couplets matching style..."
```

All templates export `(order) => string` so Lovable can tweak copy without touching code.

---

## 7  Testing & QA

* **Unit**: utils & prompt builders.
* **Integration**: E2E (Playwright) — create fixtures for each order‑type.
* **Performance**: ensure Rush tasks finish < 5 s on API.

---

## 8  Deployment Strategy

1. Ship DB migration (`order_type` columns) ➜ wait for Render rebuild.
2. Deploy BE changes behind feature flag `ORDER_TYPES_V2`.
3. Deploy FE once BE flag = true.
4. Rollback plan: switch flag off; FE gracefully degrades (default `STANDARD`).

---

## 9  Timeline (T‑shirt sizing)

| Day     | Milestone                            |
| ------- | ------------------------------------ |
| **D0**  | Branch `feature/order-types` created |
| D1–D2   | DB migration + helper method         |
| D3      | API endpoints ready                  |
| D4–D6   | Front‑end components + styling       |
| D7      | QA & bug‑bash                        |
| D8      | Deploy to staging / Vercel preview   |
| D9      | Stakeholder sign‑off                 |
| **D10** | Production deploy                    |

---

## 10  Risks & Mitigations

* **Unmapped historical products** → Default to `OTHER`, log warning.
* **Prompt quality for UPSELL** → Add manual override before sending to AI.
* **Rush SLA violations** → Auto‑ escalate to Slack if generation > 10 min.

---

## 11  Next Steps

1. Approve this plan in PR.
2. Create issues per task and assign owners.
3. Set feature flag and start migration.

---

*© 2025 JouwSong Engineering*
