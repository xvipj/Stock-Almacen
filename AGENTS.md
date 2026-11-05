# AGENTS.md

Django inventory MVP for a clothing store. The UI, domain terms, URL names, and code comments are in **Spanish**; keep new user-facing text and identifiers consistent with that. `README.md` documents the flows and demo data in detail — read it when behavior is unclear.

## Commands

Run from the repo root in PowerShell. The project venv exists at `venv/` (gitignored) with Python 3.14.3 and Django 6.1.3; call it explicitly to avoid "No module named django":

```powershell
.\venv\Scripts\python.exe manage.py runserver
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py test
```

Run that order before finishing: system check, migration drift check, tests. Current baseline is 8 passing tests in `catalog/tests.py` and `inventory/tests.py`.

Single test / single app:

```powershell
.\venv\Scripts\python.exe manage.py test inventory.tests.InventoryFlowTests.test_salida_no_deja_stock_negativo
.\venv\Scripts\python.exe manage.py test catalog
```

There is no linter, formatter, typechecker, CI, or JS build — do not invent commands for them.

Fresh setup: `manage.py migrate`, `createsuperuser`, then `manage.py seed_demo` (idempotent; uses the first superuser or creates a `bodega` user). `db.sqlite3` exists locally but is **gitignored**, and it holds demo data: do not delete or reset it without asking.

## Scaffolding (use Django commands, never hand-create generated files)

- Create new apps ONLY with `.\venv\Scripts\python.exe manage.py startapp <name>` from the repo root, so the default app structure (`apps.py`, `models.py`, `views.py`, `admin.py`, `tests.py`, `migrations/`) is preserved. Do not create these files one by one.
- After `startapp`, register the app in `INSTALLED_APPS` using its `AppConfig` path (e.g. `"<name>.apps.<Name>Config"`), then add only the extra files the app needs (`urls.py`, `forms.py`, `services.py`, `signals.py`, templates, static).
- For a brand-new Django project, use `.\venv\Scripts\python.exe -m django startproject config .` (note the trailing dot so `manage.py` stays at the repo root). Do not hand-write `manage.py`, `settings.py`, `wsgi.py`, or `asgi.py`.
- Never hand-write migration files. Always generate them with `manage.py makemigrations` and apply them with `manage.py migrate`.
- Use `manage.py createsuperuser` and custom management commands (`<app>/management/commands/`) instead of ad-hoc scripts to create users or data.
- After scaffolding, run `manage.py check` before continuing.

## Architecture

- `config/` is the Django project; `accounts`, `catalog`, `inventory`, and `dashboard` are the four apps. `catalog` owns products/variants, `inventory` owns movements/stock rules, `dashboard` only reads and caches aggregates.
- Import direction is `catalog.models -> inventory.stock` and `inventory.models -> catalog.models`. `inventory/stock.py` must stay free of model imports to keep this working; put model-aware logic elsewhere.
- **Stock is never stored.** `Variant.stock_actual` computes it from movements via `calcular_stock()`; `AJUSTE` sets the absolute value, not a delta. Never add a stock field or edit stock directly.
- Create movements through `inventory.services.registrar_movimiento()` (atomic + `select_for_update`), not ad-hoc saves. `StockMovement.save()` calls `full_clean()`, so validation errors can surface from `.save()` as well as forms.
- Stock properties iterate `movimientos`, so keep the existing `Prefetch`/`select_related` in `catalog/views.py`, `catalog/admin.py`, and `dashboard/views.py`; removing them introduces N+1 queries.
- Dashboard summary is cached for 60 s under `settings.DASHBOARD_CACHE_KEY`. `catalog/signals.py` and `inventory/signals.py` invalidate it from `post_save`/`post_delete`; bulk `QuerySet.update()` bypasses signals. `LocMemCache` is per-process — after raw SQL/shell edits, clear it or restart the server.
- Signals are connected in each app's `AppConfig.ready()`. If adding an app with signals, follow that pattern.
- `StockMovement.fecha` is `auto_now_add`; to backdate a movement, save first and then run `StockMovement.objects.filter(pk=...).update(fecha=...)`, as `seed_demo` does.
- Field normalization happens in forms only: SKU and `talla` are uppercased, `color` is title-cased. Direct ORM writes bypass this, so normalize explicitly in scripts/commands.
- Django 6 constraints use `CheckConstraint(condition=...)`, not the removed `check=` keyword.
- Categories have no public CRUD; create/edit them in `/admin/`. Logout is a POST form and must remain POST.

## UI conventions

- `templates/base.html` is the shared layout; app templates live under each app's `templates/`. CRUD forms reuse `templates/partials/form_fields.html`.
- All styling is in `static/css/app.css`, using plain CSS variables. There is no Bootstrap, Tailwind, JavaScript framework, npm, or build step — keep it that way.
- URLs use app namespaces (`catalog:`, `inventory:`, `dashboard:`, `accounts:`); use `{% url %}` / `reverse()` rather than hardcoded paths.

## Testing notes

- Use Django's built-in `TestCase`; there is no pytest setup.
- `LocMemCache` persists between `TestCase` methods. Call `cache.clear()` in `setUp` when asserting cache behavior, as `inventory/tests.py` does.
