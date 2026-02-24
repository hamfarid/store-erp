# AGENTS.md (v2026.2)

## 1. Core Agents
- **Planner:** Strategic analysis (`speckit.py analyze`).
- **Executor:** Implementation (`speckit.py implement`).
- **Reviewer:** Verification (`speckit.py verify`).

## 2. ML/AI Agents (NEW)
- **Data Engineer:** Schema validation, ETL (`roles/data_engineer.md`).
- **ML Engineer:** Training, Experimentation (`roles/ml_engineer.md`).
- **Model Reviewer:** Gatekeeper for production (`roles/model_reviewer.md`).
- **Drift Monitor:** Post-deployment surveillance (`roles/drift_monitor.md`).
- **Data Annotator:** Labeling quality assurance (`roles/data_annotator.md`).

## 3. Interaction Protocol
- **Handoff:** Explicit handoff required between stages (e.g., Data Eng -> ML Eng).
- **Artifacts:** All outputs must be versioned (DVC/MLflow) before handoff.
