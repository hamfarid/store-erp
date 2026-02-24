# Makefile — Global System v26.0.2 Diamond 32
# Unified task runner for all system operations

.PHONY: help audit setup test lint clean package deploy

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Audit & Verification ───────────────────────────────────
audit: ## Run zero-error audit
	python3 tools/zero_error_audit.py

preflight: ## Run preflight checks before deployment
	python3 tools/preflight_check.py

verify: ## Run full system verification
	python3 tools/final_verify.py

verify-imports: ## Verify all Python imports resolve
	python3 tools/verify_all_imports.py

# ─── Setup & Installation ───────────────────────────────────
setup: ## Initialize project structure and dependencies
	python3 setup_project.py

install: ## Install Python dependencies
	pip install -r requirements.txt

# ─── Code Quality ───────────────────────────────────────────
lint: ## Run linters (black + flake8 + mypy)
	black --check .
	flake8 .
	mypy .

format: ## Auto-format code with black
	black .

docstrings: ## Auto-generate missing docstrings
	python3 tools/auto_docstring.py

fix-versions: ## Update version stamps across all files
	python3 tools/fix_versions.py

# ─── Testing ────────────────────────────────────────────────
test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=. --cov-report=html

# ─── Documentation ──────────────────────────────────────────
inventory: ## Regenerate INVENTORY.md
	python3 tools/generate_inventory.py

readme: ## Regenerate README files
	python3 tools/readme_generator.py

docs-serve: ## Serve documentation locally
	mkdocs serve

# ─── System Management ──────────────────────────────────────
checkpoint: ## Create system checkpoint
	python3 tools/checkpoint_manager.py --create

security: ## Run security scan
	python3 tools/security_scan.py

clean: ## Remove __pycache__, .pyc, .DS_Store
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true

# ─── Packaging & Deployment ─────────────────────────────────
package: clean audit ## Package system into ZIP
	zip -r Global_System_v26_Diamond_32.zip . -x ".git/*" "__pycache__/*" "*.pyc" "node_modules/*" ".env"

deploy: preflight ## Deploy using docker compose
	docker compose up -d --build

# ─── GitHub ─────────────────────────────────────────────────
github-push: ## Upload to GitHub
	python3 manage_global_system.py

github-pull: ## Download from GitHub
	python3 download_from_github.py
