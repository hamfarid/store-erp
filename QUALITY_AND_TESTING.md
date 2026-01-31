## Unified linting + testing (Ai_Project)

This repo contains multiple independent projects. The recommended workflow is:

1) Run **pre-commit** for formatting/linting.
2) Run **project-specific tests** from that project directory.

### 1) Lint/format (all projects)

From the repo root:

* Install hooks (one-time): `pre-commit install`
* Run on all files (optional): `pre-commit run --all-files`
* Run only on changed files: `pre-commit run`

Ruff rules are configured in `ruff.toml` at the repo root.

### 2) Zakat backend (pytest + coverage)

Project: `3-Zakat/Zakat_Clean/backend`

Run tests:

* `cd 3-Zakat/Zakat_Clean/backend`
* `python -m pytest`

Run with coverage:

* `python -m pytest --cov=src --cov-report=term-missing --cov-report=xml:coverage.xml`

### 3) Gaara ERP (Django tests via pytest-django)

Project: `5-gaara_erp`

Pytest is configured via `5-gaara_erp/pytest.ini` (sets `DJANGO_SETTINGS_MODULE=gaara_erp.settings.test`).

Run tests:

* `cd 5-gaara_erp`
* `python -m pytest`

Run with coverage:

* `python -m pytest --cov=gaara_erp --cov-report=term-missing --cov-report=xml:coverage.xml`
