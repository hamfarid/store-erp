.PHONY: all quickcheck quickcheck-strict fullcheck pipreqs diff diff-strict test-celery test-all help

PY ?= python
PIPREQS_ARGS := --encoding utf-8 --savepath tools/requirements_autogen.txt --ignore venv,.venv,__pycache__,migrations,tests --mode compat .
CELERY_TESTS := tests/test_celery_heartbeat.py \
	tests/test_celery_health_routes.py \
	tests/test_celery_routes_integration.py

all: quickcheck

help:
	@echo "make quickcheck         - pipreqs + diff + run Celery-focused tests"
	@echo "make quickcheck-strict  - pipreqs + diff (strict) + Celery tests (CI-safe)"
	@echo "make fullcheck          - pipreqs + diff + run full pytest suite (may fail on unrelated tests)"
	@echo "make pipreqs            - regenerate tools/requirements_autogen.txt"
	@echo "make diff               - compare curated vs auto requirements"
	@echo "make diff-strict        - fail if differences are found"
	@echo "make test-celery        - run only Celery-related tests"
	@echo "make test-all           - run full pytest suite"

quickcheck: pipreqs diff test-celery

quickcheck-strict: pipreqs diff-strict test-celery

fullcheck: pipreqs diff test-all

pipreqs:
	$(PY) -m pipreqs $(PIPREQS_ARGS)

diff:
	$(PY) tools/diff_requirements.py

diff-strict:
	$(PY) tools/diff_requirements.py --strict

test-celery:
	SKIP_BLUEPRINTS=1 $(PY) -m pytest -q $(CELERY_TESTS)

test-all:
	SKIP_BLUEPRINTS=1 $(PY) -m pytest -q

