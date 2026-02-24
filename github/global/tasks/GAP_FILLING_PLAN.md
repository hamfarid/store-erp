# 🛠️ Gap Filling Plan (Global System v26 Diamond 32 Synchronized Intelligence Edition)

Based on the Master Task List, the following components are missing or incomplete and MUST be created:

## 1. Workflows (`global_system/workflows/`)
- [ ] **Create `04_feature_development_workflow.md`:** Define how The Planner breaks down a new feature and hands it to The Executor.
- [ ] **Create `05_bug_fix_workflow.md`:** Define the "Triage -> Reproduce -> Fix -> Verify" loop.

## 2. Examples (`global_system/examples/`)
- [ ] **Create `rag/vector_db_setup.md`:** A concrete example of setting up ChromaDB with Python.
- [ ] **Update `backend/api_structure.md`:** Ensure it uses FastAPI/Express best practices for 2025.

## 3. Prompts (`global_system/prompts/`)
- [ ] **Create `speckit/critique.md`:** The specific prompt for The Critic agent to use when evaluating output.

## 4. Infrastructure (`global_system/infrastructure/`)
- [ ] **Create `Dockerfile.template`:** A universal Dockerfile for Python/Node apps.
- [ ] **Create `k8s/deployment.yaml`:** A standard Kubernetes deployment template.

## 5. Memory (`global_system/memory-bank/`)
- [ ] **Populate `knowledge/best_practices/README.md`:** Singleton, Factory, Strategy (Python examples).
- [ ] **Populate `knowledge/lessons_learned/README.md`:** God Object, Spaghetti Code, Hardcoded Secrets.

## 6. Roles (`global_system/roles/`)
- [ ] **Rename `architect.md` to `planner.md`** (and update content).
- [ ] **Rename `builder.md` to `executor.md`** (and update content).
- [ ] **Rename `qa_engineer.md` to `reviewer.md`** (and update content).
