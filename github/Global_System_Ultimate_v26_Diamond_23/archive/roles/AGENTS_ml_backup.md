# AGENTS.md - ML/AI Governance (Feb 2026)

This file defines the specialized AI agents responsible for executing ML/AI projects within the Global System Ultimate framework. Each agent operates under strict governance protocols.

## 1. Agent Roster

| Agent Name | Role File | Primary Responsibility | Key Tools |
| :--- | :--- | :--- | :--- |
| **Data Engineer** | `ROLE-data-engineer.md` | Pipeline Design, ETL, Data Quality | Airflow, Spark, Great Expectations |
| **ML Engineer** | `ROLE-ml-engineer.md` | Model Architecture, Training, Registry | PyTorch, MLflow, Optuna |
| **Feature Engineer** | `ROLE-feature-engineer.md` | Feature Creation, Feature Store | Feast, Tecton, Spark |
| **Model Reviewer** | `ROLE-model-reviewer.md` | Fairness Auditing, Approval Gates | Fairlearn, SHAP, Evidently AI |
| **Drift Monitor** | `ROLE-drift-monitor.md` | Production Monitoring, Alerting | Evidently AI, Prometheus, Grafana |
| **Data Annotator** | `ROLE-data-annotator.md` | Labeling, Quality Assurance | Label Studio, Cleanlab |
| **MLOps Engineer** | `ROLE-mlops-engineer.md` | CI/CD, Infrastructure, Serving | Kubernetes, KServe, GitHub Actions |

## 2. Interaction Protocol

1.  **Task Assignment:** The **Planner** (Global System) assigns tasks to specific agents based on their role definitions.
2.  **Handoffs:** Agents must explicitly hand off artifacts (e.g., validated data, trained model) to the next agent in the pipeline.
3.  **Escalation:** Agents must escalate issues according to their defined escalation rules (e.g., bias detected -> Model Reviewer).
4.  **Verification:** All outputs must be verified against the relevant governance rules (e.g., `RULES-data-validation.yaml`) before handoff.

## 3. Governance Enforcement

*   **ALL Agents** must adhere to the **Golden Rule (EDD)** and **Silver Rule (BATS)** defined in the Core Prompt.
*   **ALL Agents** must use the **Universal Folder Map** and **Internet Search Protocol**.
*   **ALL Agents** are subject to the **5-Layer Defense System** (Active Memory, HALT, FINCH-ZK, Guardian Agents, External Hippocampus).
