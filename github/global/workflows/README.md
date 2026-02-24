# Workflows — Global System v26.0.2 Diamond 32

> Step-by-step operational workflows for all system processes.

## Core Workflows
| # | Workflow | Purpose |
|---|---------|---------|
| 01 | `01_release_workflow.md` | Release management |
| 02 | `02_security_audit_workflow.md` | Security auditing |
| 03 | `03_onboarding_workflow.md` | Team onboarding |
| 04 | `04_feature_development_workflow.md` | Feature dev lifecycle |
| 05 | `05_bug_fix_workflow.md` | Bug fix process |
| 06 | `06_code_review_workflow.md` | Code review |
| 07 | `07_incident_response_workflow.md` | Incident response |
| 08 | `08_database_migration_workflow.md` | DB migrations |
| 09 | `09_ml_ci_cd_pipeline.md` | ML CI/CD |
| 15 | `15_gold_predictor_pipeline.md` | Gold price prediction |
| 16 | `16_gaara_scan_diagnosis.md` | Plant disease diagnosis |
| 17 | `17_gaara_scan_auto_training.md` | Auto-training pipeline |

## ML Workflows (in `ml/`)
$(ls workflows/ml/*.md 2>/dev/null | while read f; do echo "- \`ml/$(basename $f)\`"; done)
