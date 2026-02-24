# Rules — ML Operations (v26.0.2 Diamond 32)

> Operational rules and constraints governing ML pipeline behavior, data handling, and model lifecycle.

## Scope
18 rule files covering model versioning, data validation, training reproducibility, serving SLAs, drift thresholds, feature store governance, experiment isolation, GPU resource allocation, GDPR compliance for ML data, and rollback criteria.

## Naming Convention
All files follow `RULES-{domain}.md` format. Each rule defines Scope, Requirements, Enforcement, and Exceptions.

## Related
- `roles/ml/` — Agents that must comply with these rules
- `workflows/ml/` — Workflows these rules constrain
- `errors/ml/` — Error catalogs for rule violations
