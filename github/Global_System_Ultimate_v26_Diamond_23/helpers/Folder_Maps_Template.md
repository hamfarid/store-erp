# Folder Maps - Project Structure (Global System Ultimate)

> **Purpose:** Complete map of project structure with purpose of each folder and file.

**Last Updated:** [DATE]
**Project:** {{PROJECT_NAME}}

---

## Project Root Structure

```
{{PROJECT_NAME}}/
├── memory-bank/            # The Project's Memory (Active Context, Decisions)
├── tools/                  # The Singularity System (Tools, Scripts)
├── knowledge/              # Knowledge Base (Rules, Workflows)
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── .env                    # Secrets (GitIgnored)
├── todo.md                 # Master Task List
└── requirements.txt        # Dependencies
```

---

## /memory-bank - The Project's Memory

**Purpose:** The brain of the autonomous engineer.

```
memory-bank/
├── activeContext.md        # Current task state
├── decisionLog.md          # Architectural choices
├── productContext.md       # Why we are building this
├── progress.md             # What is done
├── projectBrief.md         # Core requirements
└── systemContext.md        # How it works
```

## /tools - The Singularity System

**Purpose:** Automation scripts and utilities.

```
tools/
├── speckit.py              # Specification Engine
├── sentinel.py             # Quality Gatekeeper
├── augment.py              # Code Enhancer
└── ...
```

## /knowledge - Knowledge Base

**Purpose:** Rules, protocols, and workflows.

```
knowledge/
├── rules/                  # System Rules (Iron Rules, Priority Order)
├── workflows/              # Standard Operating Procedures (DevOps, Frontend)
└── templates/              # Project Templates
```

## /src - Source Code

**Purpose:** Application logic.

```
src/
├── api/                    # API Endpoints
├── core/                   # Business Logic
├── db/                     # Database Models
└── utils/                  # Helper Functions
```

## /docs - Documentation

**Purpose:** Project documentation.

```
docs/
├── API_Endpoints.md
├── DB_Schema.md
├── Architecture.md
└── Security_Model.md
```
