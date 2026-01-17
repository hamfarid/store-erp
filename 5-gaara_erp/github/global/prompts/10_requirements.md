# REQUIREMENTS GATHERING PROMPT

**FILE**: github/global/prompts/10_requirements.md | **PURPOSE**: Define project scope and requirements | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 2: Initialization (New Projects)

This prompt guides you through gathering and documenting requirements for a new project.

## Pre-Execution Checklist

- [ ] Memory system is active
- [ ] Logging is configured
- [ ] User has provided initial project description
- [ ] `docs/` folder exists

## Step 1: Gather Information

Ask the user for the following information (if not already provided):

### Project Basics
1. **Project Name**: What is the name of the project?
2. **Project Type**: Web app, mobile app, desktop app, API, library, etc.
3. **Target Users**: Who will use this system?
4. **Core Purpose**: What problem does this solve?

### Technical Stack
5. **Frontend**: React, Vue, Angular, or other?
6. **Backend**: Node.js, Python, Go, or other?
7. **Database**: PostgreSQL, MySQL, MongoDB, or other?
8. **Deployment**: Cloud provider, on-premise, or other?

### Features
9. **Must-Have Features**: What features are absolutely required?
10. **Nice-to-Have Features**: What features are optional?
11. **Out of Scope**: What features are explicitly NOT included?

### Constraints
12. **Timeline**: What is the deadline?
13. **Budget**: Are there any budget constraints?
14. **Compliance**: GDPR, HIPAA, SOC 2, or other?
15. **Performance**: Any specific performance requirements?

### Security & Authentication
16. **Authentication**: JWT, OAuth, OIDC, or other?
17. **Authorization**: RBAC, ABAC, or other?
18. **Data Sensitivity**: What type of data will be handled?

## Step 2: Document Requirements

Create the following file:

### docs/REQUIREMENTS.md

```markdown
# Project Requirements

**FILE**: docs/REQUIREMENTS.md | **PURPOSE**: Project requirements | **OWNER**: [Team] | **LAST-AUDITED**: [Date]

## Project Overview

**Name**: {{PROJECT_NAME}}
**Type**: [Web App / Mobile App / API / etc.]
**Purpose**: [Brief description]
**Target Users**: [User personas]

## Functional Requirements

### Must-Have Features (P0)
1. [Feature 1]
   - **Description**: [Details]
   - **User Story**: As a [user], I want to [action] so that [benefit]
   - **Acceptance Criteria**: [Criteria]

2. [Feature 2]
   [Same structure]

### Nice-to-Have Features (P1)
1. [Feature 1]
   [Same structure]

### Out of Scope
- [Feature 1]
- [Feature 2]

## Non-Functional Requirements

### Performance
- **Response Time**: [e.g., < 200ms for API calls]
- **Throughput**: [e.g., 1000 requests/second]
- **Concurrent Users**: [e.g., 10,000]

### Security
- **Authentication**: [JWT / OAuth / etc.]
- **Authorization**: [RBAC / ABAC / etc.]
- **Data Encryption**: [At rest / In transit]
- **Compliance**: [GDPR / HIPAA / etc.]

### Scalability
- **Horizontal Scaling**: [Yes / No]
- **Load Balancing**: [Yes / No]
- **Caching**: [Redis / Memcached / etc.]

### Reliability
- **Uptime**: [e.g., 99.9%]
- **RTO**: [e.g., < 1 hour]
- **RPO**: [e.g., < 15 minutes]

## Technical Stack

### Frontend
- **Framework**: [React / Vue / Angular]
- **Language**: [TypeScript / JavaScript]
- **Styling**: [Tailwind / MUI / etc.]

### Backend
- **Framework**: [FastAPI / Django / Express]
- **Language**: [Python / Node.js / Go]
- **API**: [REST / GraphQL / gRPC]

### Database
- **Primary**: [PostgreSQL / MySQL / MongoDB]
- **Cache**: [Redis / Memcached]
- **Search**: [Elasticsearch / etc.]

### Infrastructure
- **Cloud**: [AWS / GCP / Azure]
- **Containers**: [Docker / Kubernetes]
- **CI/CD**: [GitHub Actions / GitLab CI]

## Constraints

### Timeline
- **Start Date**: [Date]
- **End Date**: [Date]
- **Milestones**: [List]

### Budget
- [Details if applicable]

### Compliance
- [GDPR / HIPAA / SOC 2 / etc.]

## Success Criteria

1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Medium/Low | High/Medium/Low | [Strategy] |

---

**Approved By**: [Name]
**Date**: [Date]
```

## Step 3: Create Initial Task List

Based on the requirements, create `docs/Task_List.md`:

```markdown
# Task List

**FILE**: docs/Task_List.md | **PURPOSE**: Master task list | **OWNER**: [Team] | **LAST-AUDITED**: [Date]

## Phase 1: Setup
- [ ] [P0][System] Initialize project structure
- [ ] [P0][System] Set up version control
- [ ] [P0][System] Configure development environment

## Phase 2: Backend
- [ ] [P0][Backend] Set up database schema
- [ ] [P0][Backend] Implement authentication
- [ ] [P0][Backend] Create API endpoints

## Phase 3: Frontend
- [ ] [P0][Frontend] Set up component library
- [ ] [P0][Frontend] Implement authentication UI
- [ ] [P0][Frontend] Create main pages

## Phase 4: Testing
- [ ] [P0][QA] Write unit tests (≥80% coverage)
- [ ] [P0][QA] Write integration tests
- [ ] [P0][QA] Write E2E tests

## Phase 5: Documentation
- [ ] [P0][Docs] API documentation
- [ ] [P0][Docs] User documentation
- [ ] [P0][Docs] Deployment guide
```

## Step 4: Log Actions

Log to `logs/info.log`:

```json
{
  "timestamp": "2025-11-18T14:30:00Z",
  "level": "INFO",
  "message": "Requirements gathering completed",
  "details": {
    "phase": "Initialization",
    "filesCreated": ["docs/REQUIREMENTS.md", "docs/Task_List.md"],
    "nextPhase": "Planning"
  }
}
```

## Step 5: Save to Memory

Save to `.memory/checkpoints/checkpoint_phase_2_[date].md`

## Next Phase

Proceed to **Phase 3: Planning** using `12_planning.md`

---

**Completion Criteria**:
- [ ] All requirements documented
- [ ] Initial task list created
- [ ] Actions logged
- [ ] Checkpoint saved

