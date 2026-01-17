# Global Development System v14.0

**Version:** 14.0.0  
**Status:** Production Ready  
**Last Updated:** 2025-11-07

---

## 🚀 Overview

This repository contains a **comprehensive, professional global development system** designed for AI agents to autonomously develop, improve, and maintain software projects. It provides a complete, clean, and professional framework with clear guidelines, zero-tolerance constraints, and a security-first (OSF) approach.

The system is built to handle both **new projects from scratch** and the **improvement of existing projects**.

## ✨ Key Features

- **Autonomous Multi-Agent System:** Orchestrates 3 AI agents (Gemini Lead, Claude Reviewer, ChatGPT Consultant) through 7 autonomous phases.
- **Comprehensive Prompt Library:** Includes 28 specialized prompts covering all aspects of software development, from requirements gathering to deployment.
- **OSF Framework:** A security-first decision-making framework with a 35% weight on security.
- **Zero-Tolerance Constraints:** 8 non-negotiable rules to ensure code quality, security, and maintainability.
- **Advanced Memory System:** 6 types of memory for context, knowledge, and state management.
- **Structured Documentation:** A 21-file documentation structure to ensure every project is well-documented.
- **Clear Frontend/Backend Separation:** Defined components and responsibilities for both frontend and backend development.
- **Robust Error Tracking:** A system for logging, tracking, and preventing errors with 4 severity levels.

## 📁 Project Structure

The project is organized into a clear and logical directory structure:

```
.global/
├── prompts/              # 28 specialized prompts
├── roles/                # 3 AI agent roles
├── helpers/              # 5 reusable templates
├── docs/                 # 21 project documentation files
├── errors/               # Error tracking system
├── .memory/              # 6 types of memory
├── knowledge/            # 10 knowledge files
├── examples/             # 5 example projects
├── workflows/            # 7 workflow definitions
├── rules/                # 10 rule files
└── .augment/             # Augment integration
```

For a complete guide on how to use this system, please refer to the **`GLOBAL_PROFESSIONAL_CORE_PROMPT.md`** file.

## 🚀 Getting Started

To start using the system, an AI agent should:

1.  **Read** the `GLOBAL_PROFESSIONAL_CORE_PROMPT.md` to understand the entire system, its principles, and workflows.
2.  **Identify** its role by reading the corresponding file in the `roles/` directory.
3.  **Follow** the instructions provided in the core prompt for either starting a new project or improving an existing one.

### For New Projects

Follow the 7 autonomous phases, starting with `prompts/10_requirements.md`.

### For Existing Projects

Start by analyzing the existing codebase with `prompts/11_analysis.md` and creating project maps in `docs/PROJECT_MAPS.md`.

## 🧠 Core Principles

- **Security First:** Always prioritize security in all decisions.
- **Zero Tolerance:** Never violate the 8 core constraints.
- **Documentation:** Document everything. Code, decisions, and processes.
- **Testing:** Test thoroughly at all levels (unit, integration, E2E).
- **Collaboration:** Leverage the multi-agent system for development, review, and consultation.

## 🤝 Contributing

Please refer to `docs/CONTRIBUTING.md` for guidelines on how to contribute to this system.

## 📄 License

This project is licensed under the MIT License. See `docs/LICENSE.md` for details.

