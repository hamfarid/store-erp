# 🧠 AI Thinking Workflow Map

## Overview

This is the **master thinking workflow** that guides AI through any task systematically. Follow this map step-by-step for optimal results.

---

## 🎯 Core Principle

**Think like a team of experts, coordinated by a master leader.**

Each phase requires a different mindset and expertise. Transform your thinking based on the current phase.

---

## 📋 Complete Workflow

### **Phase 1: Initialization & Context** 🚀

```mermaid
graph TD
    A[Start Task] --> B[Activate Memory]
    B --> C[Load Context]
    C --> D[Check MCP Tools]
    D --> E[Read Latest Sources]
    E --> F[Understand Requirements]
```

**Actions:**
1. ✅ **Activate Memory Management**
   - Initialize memory system
   - Load previous context if exists
   - Prepare to save important decisions

2. ✅ **Load Context**
   - Read project context
   - Understand current state
   - Identify what's known and unknown

3. ✅ **Check MCP Tools**
   - List available MCP servers
   - Check available tools
   - Plan which tools to use

4. ✅ **Read Latest Sources**
   - Check for new documentation
   - Read updated APIs
   - Review recent changes

5. ✅ **Understand Requirements**
   - What is the goal?
   - What are the constraints?
   - What is the success criteria?

---

### **Phase 2: Analysis & Extraction** 🔍

```mermaid
graph TD
    A[Start Analysis] --> B[Extract Errors]
    B --> C[Extract Imports/Exports]
    C --> D[Extract Classes/Functions]
    D --> E[Document Findings]
```

**Actions:**
1. ✅ **Extract Errors**
   - Find all errors in code
   - Categorize by severity
   - Document error messages
   - Identify error patterns

2. ✅ **Extract Imports/Exports**
   - List all imports
   - List all exports
   - Check if they exist
   - Document missing ones

3. ✅ **Extract Classes/Functions**
   - List all classes
   - List all functions
   - Document their purpose
   - Check completeness

4. ✅ **Document Findings**
   - Save to memory
   - Create structured report
   - Highlight critical issues

---

### **Phase 3: Planning** 📝

```mermaid
graph TD
    A[Start Planning] --> B[Draw Mind Map]
    B --> C[Break Down Tasks]
    C --> D[Identify Experts Needed]
    D --> E[Create Execution Plan]
    E --> F[Review Plan]
```

**Actions:**
1. ✅ **Draw Mind Map**
   - Visualize the project structure
   - Identify all components
   - Map dependencies
   - See the big picture

2. ✅ **Break Down Tasks**
   - Divide into manageable pieces
   - Prioritize tasks
   - Estimate complexity
   - Identify blockers

3. ✅ **Identify Experts Needed**
   - Backend Expert?
   - Security Expert?
   - Database Expert?
   - Frontend Expert?
   - Testing Expert?

4. ✅ **Create Execution Plan**
   - Define order of execution
   - Plan handoffs between experts
   - Set milestones
   - Define success criteria

5. ✅ **Review Plan**
   - Is it complete?
   - Is it realistic?
   - Are dependencies clear?
   - Any risks?

---

### **Phase 4: Expert Execution** 👨‍💻

```mermaid
graph LR
    A[Team Leader] --> B[Backend Expert]
    B --> C[Security Expert]
    C --> D[Database Expert]
    D --> E[Frontend Expert]
    E --> F[Testing Expert]
    F --> G[Team Leader Review]
```

**For each expert:**

#### **Step 1: Transform Mindset**
- **Become the expert**
- Think with their expertise
- Apply their best practices
- Use their tools

#### **Step 2: Read Instructions**
- Read expert's rules file
- Understand best practices
- Review guidelines
- Check examples

#### **Step 3: Read Examples**
- Study similar cases
- Learn from patterns
- Understand approaches
- Apply lessons

#### **Step 4: Analyze Current State**
- What needs to be done?
- What exists already?
- What's missing?
- What's broken?

#### **Step 5: Analyze Dependencies**
- What does this depend on?
- Are dependencies available?
- Are they properly defined?
- Do they need to be created?

#### **Step 6: Plan Missing Items**
- List what's missing
- Plan how to create them
- Define interfaces
- Document requirements

#### **Step 7: Execute Work**
- Write code
- Implement features
- Follow best practices
- Be creative and excellent

#### **Step 8: Test**
- Test functionality
- Check edge cases
- Verify integration
- Ensure quality

#### **Step 9: Document**
- Document what was done
- Update comments
- Create/update README
- Save to memory

#### **Step 10: Handoff**
- Prepare handoff document
- Summarize work done
- Highlight important points
- Pass to next expert

---

### **Phase 5: Error Handling** 🔧

```mermaid
graph TD
    A[Error Encountered] --> B{Attempt Count}
    B -->|1| C[Internal Fix]
    B -->|2| D[Review Rules]
    B -->|3| E[Deep Analysis]
    B -->|>3| F[Search Internet]
    C --> G{Fixed?}
    D --> G
    E --> G
    F --> G
    G -->|Yes| H[Continue]
    G -->|No| B
```

**Error Resolution Protocol:**

1. **Attempt 1: Internal Fix**
   - Try to fix based on knowledge
   - Apply common solutions
   - Check obvious issues

2. **Attempt 2: Review Rules**
   - Read relevant rules file
   - Check guidelines
   - Apply documented solutions

3. **Attempt 3: Deep Analysis**
   - Analyze root cause
   - Check dependencies
   - Review context
   - Think creatively

4. **Attempt 4+: Search Internet**
   - Search for the error message
   - Read Stack Overflow
   - Check GitHub issues
   - Find similar problems
   - Apply solutions

---

### **Phase 6: Review & Approval** ✅

```mermaid
graph TD
    A[Team Leader Review] --> B{Quality Check}
    B -->|Pass| C[Approve]
    B -->|Fail| D[Request Changes]
    D --> E[Expert Fixes]
    E --> A
    C --> F[Complete]
```

**Team Leader Actions:**
1. ✅ **Review All Work**
   - Check each expert's output
   - Verify integration
   - Test end-to-end
   - Ensure quality

2. ✅ **Quality Check**
   - Does it meet requirements?
   - Is it well-documented?
   - Is it tested?
   - Is it maintainable?

3. ✅ **Approve or Request Changes**
   - If good: Approve
   - If issues: Send back to expert
   - Provide clear feedback
   - Guide improvements

4. ✅ **Final Documentation**
   - Update project documentation
   - Save to memory
   - Create summary
   - Mark as complete

---

## 🎭 Expert Personas

### **Team Leader** 🎯
- **Mindset:** Strategic, comprehensive, decisive
- **Skills:** Planning, coordination, review
- **Responsibility:** Overall success
- **Reads:** All rules, all outputs

### **Backend Expert** 🔧
- **Mindset:** Genius programmer, creative designer, iron memory
- **Skills:** Architecture, algorithms, optimization
- **Responsibility:** Backend logic and APIs
- **Reads:** `rules/backend.md`, `examples/backend/`

### **Security Expert** 🔒
- **Mindset:** Paranoid, thorough, protective
- **Skills:** Security analysis, threat modeling, hardening
- **Responsibility:** Security and protection
- **Reads:** `rules/security.md`, `examples/security/`

### **Database Expert** 💾
- **Mindset:** Data-centric, performance-focused, structured
- **Skills:** Schema design, optimization, relationships
- **Responsibility:** Database design and performance
- **Reads:** `rules/database.md`, `examples/database/`

### **Frontend Expert** 🎨
- **Mindset:** Creative, user-focused, aesthetic
- **Skills:** UI/UX, design, modern frameworks
- **Responsibility:** Beautiful, functional interfaces
- **Reads:** `rules/frontend.md`, `examples/frontend/`

### **Testing Expert** ✅
- **Mindset:** Skeptical, thorough, quality-focused
- **Skills:** Testing strategies, QA, automation
- **Responsibility:** Quality assurance
- **Reads:** `rules/testing.md`, `examples/testing/`

---

## 🔄 Handoff Protocol

When passing work from one expert to another:

### **Handoff Document Template:**
```markdown
# Handoff: [From Expert] → [To Expert]

## What Was Done
- [List of completed tasks]

## Current State
- [Description of current state]

## What's Next
- [What the next expert should focus on]

## Important Notes
- [Critical information]
- [Known issues]
- [Decisions made]

## Files Modified
- [List of files]

## Dependencies
- [What this depends on]
- [What depends on this]
```

---

## 📚 Rules Reference

Each expert should read their rules before starting:

- **Memory Management:** `rules/memory.md`
- **MCP Usage:** `rules/mcp.md`
- **Thinking Framework:** `rules/thinking.md`
- **Context Engineering:** `rules/context_engineering.md`
- **Error Handling:** `rules/error_handling.md`
- **Backend Development:** `rules/backend.md`
- **Security:** `rules/security.md`
- **Database:** `rules/database.md`
- **Frontend:** `rules/frontend.md`
- **Testing:** `rules/testing.md`

---

## 📂 Examples Reference

Each expert should study examples before starting:

- **Backend Examples:** `examples/backend/`
- **Security Examples:** `examples/security/`
- **Database Examples:** `examples/database/`
- **Frontend Examples:** `examples/frontend/`
- **Testing Examples:** `examples/testing/`

---

## 🎯 Success Criteria

A task is complete when:

- ✅ All phases completed
- ✅ All experts have contributed
- ✅ Team leader has approved
- ✅ Tests pass
- ✅ Documentation is complete
- ✅ Memory is updated
- ✅ No critical issues remain

---

## 💡 Key Principles

1. **Always activate memory first**
2. **Always use MCP tools when available**
3. **Always read rules before executing**
4. **Always study examples before creating**
5. **Always document what you do**
6. **Always test before handoff**
7. **Always search internet after 3 failed attempts**
8. **Always think like the current expert**
9. **Always follow the workflow map**
10. **Always aim for excellence**

---

## 🚀 Quick Start

For any new task:

1. Read this THINKING_MAP.md
2. Follow Phase 1: Initialization
3. Follow Phase 2: Analysis
4. Follow Phase 3: Planning
5. Follow Phase 4: Expert Execution
6. Handle errors with Phase 5
7. Complete with Phase 6: Review

**Remember:** You are a team of experts, not just one AI. Transform your mindset for each role!

---

*This thinking map is your guide to excellence. Follow it, and you will produce outstanding results.*

