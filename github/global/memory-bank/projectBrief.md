# Project Brief — Global System v26 Diamond 32 (v26.0 Diamond 9)

> **Purpose**: Define the project mission, objectives, and success criteria
> **Audience**: All agents entering the project for the first time
> **Version**: v26.0.2 (Diamond 32)

## Mission

To establish a Global Standard for AI-driven software development, ensuring that every project starts with a secure, scalable, and intelligent foundation. The Global System v26 Diamond 32 provides a complete governance framework that guides AI agents through the entire software development lifecycle — from architecture through deployment and monitoring.

## Core Objectives

-   **Eliminate Friction**: Provide a streamlined setup process for AI agents. Any agent entering a project governed by this framework can immediately understand the project state, applicable rules, and their responsibilities by reading `AGENTS.md` and the `memory-bank/` directory.
-   **Enforce Quality**: Automate code reviews, security checks, and compliance validation through integrated tools (`speckit.py`, pre-commit hooks, CI/CD pipeline). Quality gates at every stage prevent defective code from reaching production.
-   **Preserve Context**: Maintain a persistent memory of decisions, lessons learned, and project state in the `memory-bank/` directory. This ensures continuity across sessions and prevents knowledge loss when agents change.
-   **Scale Autonomously**: Enable AI agents to manage complex, multi-module projects with minimal human intervention through clear role definitions, escalation protocols, and coordinated multi-agent workflows.
-   **Govern ML/AI Systems**: Provide comprehensive governance for machine learning projects including model lifecycle management, explainability requirements (GradCAM), drift detection, and structured error catalogs. The plant disease detection pipeline serves as the reference implementation.

## Success Criteria

-   **Zero Critical Errors**: No crashes, security vulnerabilities, or data integrity issues in core governance tools and production deployments. All known error patterns documented in `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md`.
-   **100% Compliance**: All files in the framework adhere to the Global System v26 Diamond 32 v26 standard. No skeletal files, no broken cross-references, no version inconsistencies.
-   **Reproducibility**: Any experiment, deployment, or analysis can be fully reproduced from logged configurations and documented decisions.
-   **Version Agnostic**: The system can be upgraded from one version to the next without breaking existing projects. Migration guides accompany every major version change.

## Current Focus (v26.0 Diamond 9)

The v26 Diamond 9 release focuses on multi-view ML pipeline governance, expanded role definitions, comprehensive error catalogs for deep learning and drift detection, and ensuring all framework files exceed minimum content depth requirements.

## Key Entry Points

The primary governance document is `AGENTS.md`. Bootstrap guide: `BOOTSTRAP_v26.0.md`. Claude Code compatibility: `CLAUDE.md`. Iron rules: `rules/00-iron-rules.md`. ML governance: `rules/ml/` directory.
