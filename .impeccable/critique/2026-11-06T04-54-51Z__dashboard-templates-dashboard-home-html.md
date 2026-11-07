---
target: dashboard/templates/dashboard/home.html
total_score: 29
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 2
target_identity: "file:C:\\Users\\xavie\\Desktop\\Stock-Almacen\\dashboard\\templates\\dashboard\\home.html"
target_fingerprint: "sha256:e98b29900f13317ce65d447b7d785d35e1c0545a2de53aa6df0cef08bd45e09d"
target_path: "C:\\Users\\xavie\\Desktop\\Stock-Almacen\\dashboard\\templates\\dashboard\\home.html"
timestamp: 2026-11-06T04-54-51Z
slug: dashboard-templates-dashboard-home-html
---
# Critique — Dashboard · Stock Almacén

Target: `dashboard/templates/dashboard/home.html` (dashboard landing, plus shared shell `templates/base.html` and `static/css/app.css`)

Method: ⚠️ DEGRADED — single-context (sub-agent nesting unavailable: depth limit reached). Assessment A was completed before Assessment B ran.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Freshness chip exists, but “Datos frescos / Desde caché” never says when the data was last updated. |
| 2 | Match System / Real World | 3 | Strong Spanish domain voice, undermined by “LocMemCache” in a tooltip and “MVP … con Django” in the footer. |
| 3 | User Control and Freedom | 3 | Clear navigation and exit, but no way to refresh the cached view or reach the full low-stock list. |
| 4 | Consistency and Standards | 4 | Cohesive tokens, one primary action, predictable components; only the third metric’s top-right slot changes meaning. |
| 5 | Error Prevention | 3 | Stock rules are enforced in the model and forms; the dashboard itself is read-only. |
| 6 | Recognition Rather Than Recall | 3 | Labels and variant context are visible; the core lookup still requires remembering Catálogo → search → product. |
| 7 | Flexibility and Efficiency | 2 | No search, shortcuts, sorting, bulk actions, or complete replenishment view from the landing screen. |
| 8 | Aesthetic and Minimalist Design | 4 | Disciplined density, restrained color, tabular numerals, no decorative noise. |
| 9 | Error Recovery | 3 | Form errors are specific and preserve work; no error surface exists on the dashboard. |
| 10 | Help and Documentation | 1 | No contextual help; the only explanation is an inaccessible, technical `title` tooltip. |
| **Total** | | **29/40** | **Good (72.5%)** |

## Design Specificity Verdict

**LLM assessment:** Specific in voice and surface, generic in composition. The page is recognizably “El Mostrador Ordenado”: tabular numerals, 10px uppercase labels, flat 1px borders, one indigo accent, dense rows. But swap the Spanish labels for an electronics stockroom and the layout still works unchanged: sidebar, three KPI cards, recent-movements table, 340px alert rail. The clothing-specific signal is limited to the `talla / color` subline and the stock/minimum pair. The low-stock row is the most authored element; the three metric cards are the most category-default. For an Operate surface, restraint is correct — this is not a demand for novelty. The missed opportunity is to let the variant axis organize the page, e.g. a replenishment list grouped by product with size/color chips and a “faltan N” deficit. Verdict: **grounded at the surface level, interchangeable at the layout level.**

**Deterministic scan:** Two passes. The template scan (12 findings, all advisory, `design-system-color` / `rgb(0,0,0)`) is **not usable**: the detector could not resolve `{% static 'css/app.css' %}`, so it saw every template as unstyled black text. All 12 are false positives. The rendered-page scan (Django test client + inlined CSS) returned **39 findings: 36 warnings, 3 advisories**:
- `low-contrast` — 8 (6 warnings, 2 advisories). Real warnings: `#9aa1ae` on white at **2.6:1** and on canvas at **2.4:1**, used by “mín. N”, metric context labels, nav group labels, and footer. The two `#6b7280` on `#f5f6fa` advisories are **4.48:1**, a rounding-level miss.
- `undersized-ui-text` — 26 (25 warnings, 1 advisory). Table headers 10px, badges 10.5px, “mín. N” 10.5px, cache chip 10.5px, metric labels 10px. This is one systemic size token repeated, not 26 separate defects.
- `tiny-text` — 3 warnings for 11.5px supporting copy (metric hints, cell subtitles).
- `cramped-padding` — 1 warning for `.sidebar-footer`; **false positive**, it has 16px `padding-top` above the border.
- `kicker-above-heading` — 1 warning for “Resumen general” above “Hola, admin”; **valid**, it adds neither location nor information.

The detector confirmed the microcopy legibility problem I found in the render, but missed the alert hierarchy, the truncated list, the mobile table clipping, and the cache jargon. The 9px “Almacén” brand wordmark finding is also a false positive; it is a logo, not functional text.

**Visual overlays:** No user-visible overlay. The target is a Django template behind authentication, and no browser automation/injection channel was exposed; a `[Human]` tab and console overlay were not available. Evidence instead came from headless Chrome screenshots at 1440×900, 1440×1800, 1024×900, and a CDP-emulated 390×844 viewport, with the stylesheet inlined.

## Overall Impression

This is a disciplined, legible operations dashboard that already feels like a tool, not a template. The biggest opportunity is to make the alert system as serious as the ledger: low stock is currently a side rail that falls below the fold on narrow screens and stops at five with no way to see the rest. The micro-label system is the visual signature, but at 10–10.5px and 2.6:1 it is also the accessibility weak point.

**Cognitive load:** 2 failures out of 8 — **moderate**. Hierarchy: recent movements dominate while the actionable alert list is secondary. Progressive disclosure: only five alerts are shown, with no expansion path. The other six checks pass: related data is grouped, the header has one primary action, stock and minimum sit together, and no memory bridge is required.

**Emotional journey:** Peak at the greeting and three clear numbers; the amber “5” immediately says something needs attention, and the low-stock rows are calm and specific. Valley on a phone or tablet: after three metric cards and ten movement rows, the first alert finally appears — the “5” is a promise the screen does not keep immediately. If there are more than five alerts, “Y N variantes más” is a dead end. Reassurance is strong in the “Sin alertas” state (green check, plain sentence), and the amber card is noticeable without alarm. The cache chip introduces low-grade doubt (“is this stale?”) without giving the information needed to resolve it.

## What's Working

1. **The low-stock row is the best composition on the page.** Product, `talla / color`, stock, and minimum are co-located; the whole row is a link; the amber is a tinted triad (wash + border + dark text), not a saturated block. It answers “what needs reordering?” in one scan.
2. **Table craft earns trust.** Tabular numerals, right-aligned quantities, signed values (`+30`, `-2`, `=N`), and text-plus-color badges make the ledger readable at a glance. The movement table reads as a record, not a list of cards.
3. **State design is complete.** Empty movements get an icon, a heading, a sentence, and an action; empty low stock gets “Sin alertas” and a green check; Django messages use `role="status"`. The screen does not leave the user guessing what an empty state means.

## Priority Issues

### [P1] “Stock bajo” is incomplete and loses the race on narrow screens

**What:** The card shows only the first five low variants. With more than five, the footnote “Y N variantes más” is plain text with no link or destination. At ≤1120px the entire aside drops below the 10-row movement table; at 390px the page is 2,313px tall and the first alert appears roughly 1,600px down, after three metric cards and ten movement rows.

**Why it matters:** The dashboard’s operational job is “what needs reordering?” The user can see the count but not the complete list, and on the device most likely used on the floor the list is off-screen. That turns an alert into a report.

**Fix:** Make the alert list a first-class target. At ≤1120px, order the aside before the movements card (grid `order` or source order). When `total_bajos > 5`, add a “Ver todas” link to a filtered catalog/inventory view; if no such view exists, create one rather than ending on a count. Consider letting the list grow to 10 on desktop.

**Suggested command:** `/impeccable shape` (plan the all-low-stock view) + `/impeccable layout` (responsive order).

### [P1] The micro-label system crosses from style into illegibility

**What:** `--muted-2` (`#9aa1ae`) on white is **2.6:1**, and on the canvas **2.4:1**. It carries “mín. N”, the metric context labels (“Catálogo”, “Existencias”, “Requiere atención”), nav group labels, and the footer. Functional text at 10–10.5px includes table headers, badges, “mín. N”, and the cache chip. The detector returned 6 warning-level contrast findings and 25 warning-level undersized-text findings.

**Why it matters:** The smallest, lowest-contrast text carries the interpretation of the numbers: what the column means and what the minimum is. On a laptop at 100% zoom or a phone in a bright stockroom, this is the first text to disappear. WCAG AA requires 4.5:1 for normal text; 2.4–2.6 is far below.

**Fix:** Darken the micro-label token to at least `#6b7280` (≈4.8:1 on white) or a new `#5f6674`; reserve `--muted-2` for non-essential decoration. Raise functional micro-text to 11px minimum — table headers, badges, and “mín.” — or 12px for the minimum. Keep the uppercase tracking; size and contrast are the problem, not the style. If the design system insists on 10px, record that as an explicit legibility tradeoff, not an accident.

**Suggested command:** `/impeccable audit` (contrast and legibility) + `/impeccable typeset` (scale).

### [P2] The mobile movement table hides the audit trail with no scroll cue

**What:** At 390px the table is 471px wide inside a 348px wrapper. “Usuario” is clipped and “Fecha” is completely off-screen. The wrapper scrolls, but there is no fade, sticky first column, or “desliza” cue. Rows also wrap product names onto two lines, making the table taller and denser than the desktop version.

**Why it matters:** The table’s value is the audit trail: who moved what and when. On a phone the date — the thing that makes the trail auditable — is invisible unless the user guesses to swipe. Silent clipping reads as missing data.

**Fix:** At ≤760px, drop “Usuario” (it is the same account in a single-store MVP) and show the date under the product or as a second line; or switch to stacked rows with product/variant, type, quantity, user, and date. If the table stays, add a visible scroll affordance and a sticky first column.

**Suggested command:** `/impeccable adapt`.

### [P2] The cache chip speaks developer, and its explanation is inaccessible

**What:** “Datos frescos / Desde caché” is a system concept; the `title` reads “Los indicadores se guardan 60 segundos en LocMemCache”. A `title` on a non-focusable `<span>` is not reachable by keyboard or screen reader, and touch users cannot hover. The chip also uses the same green dot for both fresh and cached states.

**Why it matters:** A store clerk does not need to know about LocMemCache, and a 60-second cache is invisible in practice. The chip adds a decision (“is this stale?”) without the information needed to answer it. For keyboard and screen-reader users, the only explanation is unavailable.

**Fix:** Remove the chip (writes already invalidate the cache), or replace it with human freshness: “Actualizado hace menos de 1 min” plus a visible timestamp. Make it a real focusable element if the detail matters, and delete “LocMemCache” from user-facing copy.

**Suggested command:** `/impeccable clarify`.

### [P2] The dashboard cannot answer the counter question directly

**What:** The primary job in `PRODUCT.md` is “¿cuánto hay de esta talla y este color?” The dashboard shows aggregate totals, recent movements, and low stock, but no product or variant search. The path is Catálogo → search → product → variant. The landing screen has no lookup field.

**Why it matters:** The dashboard is the screen after login; a clerk with a garment in hand has to leave it and re-find the product. That is the most frequent task and the biggest efficiency loss, which is why Flexibility scores 2.

**Fix:** Add a compact search field in the topbar or above the movement table (“Buscar producto o SKU”) that submits to the catalog filtered by `q`, or at minimum a “Buscar en catálogo” link in the header. Keep the one-primary-action rule: search is a field, not a second primary button.

**Suggested command:** `/impeccable shape`.

## Persona Red Flags

**Alex (Power User):** No keyboard shortcut for “Registrar movimiento”; no `/` search; the movement table cannot be sorted or filtered; low-stock rows cannot be multi-selected for a replenishment list. The five-row cap means Alex cannot scan the full queue without leaving. Expects a hotkey and a quick lookup, finds neither.

**Sam (Accessibility / keyboard):** The active nav state is visual only — no `aria-current="page"`. The cache tooltip is a `title` on a non-focusable span, so it never reaches the keyboard or screen reader. “mín. N” is 10.5px at 2.6:1; table headers are 10px. At 390px the table already scrolls horizontally and the date leaves the viewport; 200% zoom makes it worse. The mobile nav is a horizontal scroller with “Administración” off-screen and no visible cue.

**Marcela (project-specific — encargada del conteo):** Standing in the stockroom with a phone in one hand. The low-stock list is about 1,600px below the top, after ten movement rows; she scrolls past the audit trail to find what to count. The table needs a horizontal swipe to see the date, so she may think the movement has no date. “mín. 2” is tiny and low contrast, so she subtracts in her head. She cannot search for the garment in her hand from this screen.

## Minor Observations

- “Resumen general” above “Hola, admin” is a filler eyebrow; the detector’s kicker ban applies. Remove it or replace it with a real locator/date. The eyebrow pattern works on “Catálogo / Producto”; here it says nothing.
- The third metric’s top-right slot switches from a category (“Catálogo”, “Existencias”) to a status (“Requiere atención”), breaking the slot’s meaning. A consistent “Reposición” would preserve the pattern and leave status to the card treatment.
- Low-stock rows show “mín. 2” but not the deficit. “Faltan 1” or “En mínimo” would remove the subtraction and make the urgency explicit.
- `th` elements lack `scope="col"`; the table has an h2 but no `caption`. Add `scope` for screen readers.
- The footer “Stock Almacén · MVP de inventario con Django” is developer language in an Operate surface; replace it with the store name or a quiet version string.
- The 4.48:1 header text is a borderline miss; the same token darkening that fixes the P1 contrast issue resolves it.
- Dates like “04 Nov, 10:59” are fine for the last ten movements but omit the year; acceptable at this scope, worth revisiting if the table ever shows older history.

## Questions to Consider

- What if the dashboard were organized around “what needs action today” rather than “what happened recently”?
- What if the low-stock list were the main column and the movement table the side rail?
- What if the alert row said “faltan 2” instead of “mín. 3”?
- What if the counter lookup lived in the topbar on every screen, not behind Catálogo?
- What if the micro-label system used 11px and a darker gray — what would it lose?
