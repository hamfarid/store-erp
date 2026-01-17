# 🗺️ Mind Maps - Complete System

**Version:** 9.0.0  
**Last Updated:** 2025-11-04

---

## 📋 Table of Contents

1. [System Architecture Mind Map](#system-architecture-mind-map)
2. [Memory System Mind Map](#memory-system-mind-map)
3. [Team Structure Mind Map](#team-structure-mind-map)
4. [Workflow Mind Maps](#workflow-mind-maps)
5. [Decision Trees](#decision-trees)

---

## 🏗️ System Architecture Mind Map

```
                    GLOBAL GUIDELINES v9.0.0
                              |
        +---------------------+---------------------+
        |                     |                     |
   CORE PROMPT          ARCHITECTURE            WORKFLOWS
        |                     |                     |
        |                     |                     |
   +----+----+          +-----+-----+         +-----+-----+
   |         |          |           |         |           |
THINKING  EXPERTS   MEMORY      RULES     SPECIFIC   EXAMPLES
  MAP       |       SYSTEM        |       WORKFLOWS     |
            |          |          |           |         |
     +------+------+   |    +-----+-----+     |    +----+----+
     |      |      |   |    |     |     |     |    |    |    |
  Backend Security DB  |  Memory MCP Think   |  Backend API DB
  Expert  Expert  Expert| Expert Expert Expert| Examples Examples
                        |                     |
                   +----+----+           +----+----+
                   |    |    |           |    |    |
                Working Short Long    API   ML  Middleware
                Memory  Term  Term   Workflow Workflow
```

---

## 🧠 Memory System Mind Map

```
                        MEMORY SYSTEM
                              |
        +---------------------+---------------------+
        |                     |                     |
    HIERARCHY             STORAGE              OPERATIONS
        |                     |                     |
        |                     |                     |
   +----+----+          +-----+-----+         +-----+-----+
   |    |    |          |     |     |         |     |     |
Working Short Long   In-Context Cache DB    Save Retrieve Update
Memory  Term  Term      |      |     |
   |     |     |        |      |     |
   |     |     |     Context Redis PostgreSQL
   |     |     |     Window
   |     |     |
   |     |     +------ Project Knowledge
   |     |             User Preferences
   |     |             Historical Decisions
   |     |
   |     +------------ Session State
   |                   Recent Interactions
   |                   Temporary Decisions
   |
   +------------------ Current Task
                       Active Expert
                       Immediate Context
```

---

## 👥 Team Structure Mind Map

```
                        TEAM LEADER
                              |
                    (Coordinates Everything)
                              |
        +---------------------+---------------------+
        |                     |                     |
    PLANNING              EXECUTION             REVIEW
        |                     |                     |
        |                     |                     |
   Mind Map              Assign Experts        Quality Check
   Requirements          Monitor Progress      Approve/Reject
   Create Plan           Handle Handoffs       Final Decision
        |                     |                     |
        |                     |                     |
        |          +----------+----------+          |
        |          |          |          |          |
        |      Backend    Security   Database       |
        |      Expert     Expert     Expert         |
        |          |          |          |          |
        |          |          |          |          |
        |      Frontend   Testing    DevOps         |
        |      Expert     Expert     Expert         |
        |          |          |          |          |
        +----------+----------+----------+----------+
                              |
                         DELIVERABLE
```

---

## 🔄 Workflow Mind Maps

### **API Development Workflow**

```
                    API DEVELOPMENT
                          |
        +-----------------+-----------------+
        |                 |                 |
    INITIALIZE         DESIGN          IMPLEMENT
        |                 |                 |
   Memory+MCP         Endpoints          Models
   Requirements       Request/Response   Serializers
   Mind Map           Error Handling     Views
        |                 |                 |
        +--------+--------+--------+--------+
                 |                 |
              SECURE            TEST
                 |                 |
           Authentication      Unit Tests
           Authorization       Integration
           Rate Limiting       Security Tests
           Input Validation    Performance
                 |                 |
                 +--------+--------+
                          |
                      DOCUMENT
                          |
                    API Docs
                    Examples
                    README
                          |
                      DEPLOY
```

### **ML/AI Development Workflow**

```
                    ML/AI DEVELOPMENT
                          |
        +-----------------+-----------------+
        |                 |                 |
      DATA            PREPARE           TRAIN
        |                 |                 |
    Collect           Clean             Choose Model
    Validate          Transform         Set Hyperparams
    Explore           Feature Eng       Train
        |                 |                 |
        +--------+--------+--------+--------+
                 |                 |
             EVALUATE          DEPLOY
                 |                 |
            Metrics           Export Model
            Tune              Create API
            Validate          Monitor
                 |                 |
                 +--------+--------+
                          |
                      MONITOR
                          |
                    Performance
                    Drift Detection
                    Retrain
```

### **Authentication Workflow**

```
                    AUTHENTICATION
                          |
        +-----------------+-----------------+
        |                 |                 |
      DESIGN          IMPLEMENT          SECURE
        |                 |                 |
    Choose Method     User Model        Hash Passwords
    (JWT/Session)     Registration      Secure Tokens
    Permissions       Login/Logout      Rate Limiting
        |                 |                 |
        +--------+--------+--------+
                          |
                        TEST
                          |
                    All Scenarios
                    Security Tests
                    Performance
                          |
                      DEPLOY
```

### **Deployment Workflow**

```
                      DEPLOYMENT
                          |
        +-----------------+-----------------+
        |                 |                 |
     PREPARE           BUILD            DEPLOY
        |                 |                 |
    Environment       Docker/Build      Push to Server
    Migrations        Run Tests         Start Services
    Dependencies      Create Release    Health Check
        |                 |                 |
        +--------+--------+--------+
                          |
                       VERIFY
                          |
                    Smoke Tests
                    Monitor Logs
                    Check Metrics
                          |
                      MONITOR
                          |
                    Application
                    Errors
                    Performance
```

### **Maintenance Workflow**

```
                      MAINTENANCE
                          |
        +-----------------+-----------------+
        |                 |                 |
     MONITOR          IDENTIFY          PRIORITIZE
        |                 |                 |
    Metrics           Bugs              High/Low
    Logs              Performance       Impact/Urgency
    Alerts            Security          Matrix
        |                 |                 |
        +--------+--------+--------+--------+
                 |                 |
               FIX              DEPLOY
                 |                 |
           Reproduce         Create PR
           Root Cause        Review
           Implement         Merge
           Test              Verify
                 |                 |
                 +--------+--------+
                          |
                       PREVENT
                          |
                    Add Tests
                    Update Docs
                    Improve Monitoring
```

---

## 🌳 Decision Trees

### **When to Use Which Expert?**

```
Task Type?
    |
    +-- Backend/API? ---------> Backend Expert
    |
    +-- Security? ------------> Security Expert
    |
    +-- Database Design? -----> Database Expert
    |
    +-- Frontend/UI? ---------> Frontend Expert
    |
    +-- Testing? -------------> Testing Expert
    |
    +-- Deployment? ----------> DevOps Expert
    |
    +-- Complex/Multiple? ----> Team Leader (coordinates)
```

### **When to Save to Memory?**

```
Event Type?
    |
    +-- Task Start? ----------> YES (Save context)
    |
    +-- Decision Made? --------> YES (Save decision + rationale)
    |
    +-- Milestone Reached? ----> YES (Save progress)
    |
    +-- Error Occurred? -------> YES (Save error + context)
    |
    +-- Solution Found? -------> YES (Save solution)
    |
    +-- Expert Handoff? -------> YES (Save handoff document)
    |
    +-- Task Complete? --------> YES (Archive everything)
```

### **When to Use MCP?**

```
Need External Tool?
    |
    +-- File Operations? ------> YES (filesystem MCP)
    |
    +-- Database Query? -------> YES (database MCP)
    |
    +-- Web Scraping? ---------> YES (playwright MCP)
    |
    +-- Cloud Operations? -----> YES (cloudflare MCP)
    |
    +-- Code Analysis? --------> YES (serena MCP)
    |
    +-- Error Tracking? -------> YES (sentry MCP)
    |
    +-- Any External API? -----> YES (check available MCPs)
```

### **Error Handling Decision Tree**

```
Error Occurred?
    |
    +-- Save Error to Memory
    |
    +-- Attempt < 3?
        |
        +-- YES: Try Known Solution
        |   |
        |   +-- Worked? --------> Continue
        |   |
        |   +-- Failed? --------> Try Next Solution
        |
        +-- NO (3+ attempts):
            |
            +-- Search Internet
            |
            +-- Found Solution? --> Apply & Save
            |
            +-- Still Failed? ---> Ask User for Help
```

### **Which Workflow to Use?**

```
Project Type?
    |
    +-- API Development? ------> api_development.md
    |
    +-- ML/AI Project? --------> ml_ai_development.md
    |
    +-- Middleware Needed? ----> middleware_development.md
    |
    +-- Flask/Django Module? --> blueprint_development.md
    |
    +-- Need Authentication? --> authentication.md
    |
    +-- Ready to Deploy? ------> deployment.md
    |
    +-- Ongoing Maintenance? --> maintenance.md
    |
    +-- Custom/Complex? -------> Combine workflows
```

---

## 🎯 Expert Selection Mind Map

```
                    TASK ANALYSIS
                          |
        +-----------------+-----------------+
        |                 |                 |
    TECHNICAL         SECURITY          CREATIVE
        |                 |                 |
        |                 |                 |
   +----+----+       +----+----+       +----+----+
   |         |       |         |       |         |
Backend   Database Security  Testing Frontend  UX/UI
Expert    Expert   Expert   Expert   Expert   Expert
   |         |       |         |       |         |
   |         |       |         |       |         |
API       Schema  Audit     Unit    Design   Colors
Logic     Design  Pentest   Tests   Layout   Flow
Models    Optimize Secure   E2E     Components
Views     Queries  Validate Coverage Responsive
```

---

## 🔄 Handoff Process Mind Map

```
                    EXPERT HANDOFF
                          |
        +-----------------+-----------------+
        |                 |                 |
   EXPERT A           HANDOFF          EXPERT B
   (Completes)        DOCUMENT         (Continues)
        |                 |                 |
        |                 |                 |
   Create Summary    Save to Memory    Retrieve Document
   Document Work     Include:          Load Context
   Note Issues       - What done       Understand State
   Prepare Files     - Current state   Continue Work
        |             - Files changed      |
        |             - Important notes    |
        |             - Next steps         |
        |                 |                 |
        +--------+--------+--------+--------+
                          |
                    TEAM LEADER
                    (Monitors)
                          |
                    Verify Handoff
                    Ensure Continuity
                    Track Progress
```

---

## 📊 Quality Gates Mind Map

```
                    QUALITY GATES
                          |
        +-----------------+-----------------+
        |                 |                 |
      CODE              SECURITY          TESTING
        |                 |                 |
        |                 |                 |
   Standards         Vulnerabilities   Coverage
   Documentation     Authentication    All Tests Pass
   Comments          Authorization     Performance
   Clean             Input Validation  Edge Cases
        |                 |                 |
        +--------+--------+--------+--------+
                 |                 |
            PERFORMANCE        DOCUMENTATION
                 |                 |
            Response Time      API Docs
            Resource Usage     README
            Scalability        Examples
                 |                 |
                 +--------+--------+
                          |
                    ALL PASS?
                          |
                    +-----+-----+
                    |           |
                  YES          NO
                    |           |
                APPROVE      REJECT
                    |           |
                DEPLOY      FIX ISSUES
```

---

## 🎨 Frontend Development Mind Map

```
                FRONTEND DEVELOPMENT
                          |
        +-----------------+-----------------+
        |                 |                 |
      DESIGN            BUILD            POLISH
        |                 |                 |
        |                 |                 |
   Wireframes        Components        Animations
   Mockups           Pages             Transitions
   Colors            Routing           Optimization
   Typography        State Mgmt        Accessibility
        |                 |                 |
        +--------+--------+--------+--------+
                 |                 |
              TEST            RESPONSIVE
                 |                 |
            Unit Tests       Mobile
            E2E Tests        Tablet
            Visual Tests     Desktop
                 |                 |
                 +--------+--------+
                          |
                      DEPLOY
```

---

*Use these mind maps to visualize and navigate the entire system.*

