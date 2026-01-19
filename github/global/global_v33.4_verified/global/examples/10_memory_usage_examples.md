# Memory (`.memory/`) Usage Examples

## Overview
This document provides **practical, real-world examples** of how to use the `.memory/` directory to maintain your working memory. Memory usage is **MANDATORY** for all projects.

---

## 📁 Memory Directory Structure

```
.memory/
├── conversations/          # All user interactions
│   ├── 20251107_session_1.md
│   └── 20251107_session_2.md
├── decisions/              # All significant decisions
│   ├── database_choice_20251107.md
│   ├── framework_choice_20251108.md
│   └── architecture_decision_20251109.md
├── checkpoints/            # Project state at each phase
│   ├── phase_1_analysis_complete.md
│   ├── phase_2_planning_complete.md
│   └── phase_3_implementation_complete.md
├── context/                # Current working context
│   └── current_task.md
├── learnings/              # Lessons learned
│   └── what_worked_what_didnt.md
└── references/             # Quick reference notes
    └── api_endpoints.md
```

---

## 💬 Example 1: Saving Conversations

### Scenario
User asks you to build an e-commerce platform.

### How to Save the Conversation

#### Step 1: Create Conversation File
```bash
# Create a timestamped conversation file
cat > .memory/conversations/20251107_ecommerce_project.md << 'EOF'
# Conversation: E-Commerce Project

## Date: 2025-11-07 14:30
## Session ID: session_001

---

### User Request
> "Build an e-commerce platform with user authentication, product catalog, shopping cart, and payment integration."

### My Response
> "Understood. I will build a full-stack e-commerce platform with the following features:
> 1. User authentication (JWT)
> 2. Product catalog (with search and filters)
> 3. Shopping cart (persistent)
> 4. Payment integration (Stripe)
> 5. Admin dashboard
>
> Tech stack:
> - Frontend: React + TypeScript
> - Backend: Node.js + Express
> - Database: PostgreSQL
> - Payment: Stripe API
>
> I will proceed with the 7-phase workflow."

---

### Follow-up Questions
**User:** "Can you add email notifications?"
**Me:** "Yes, I will add email notifications for:
- Order confirmation
- Shipping updates
- Password reset
I will use SendGrid for email delivery."

---

### Key Decisions Made
1. Chose PostgreSQL over MongoDB (see `.memory/decisions/database_choice_20251107.md`)
2. Chose Stripe over PayPal (better API, lower fees)
3. Chose SendGrid for emails (reliable, good free tier)

---

### Next Steps
1. Phase 1: Requirements gathering (DONE)
2. Phase 2: Planning (IN PROGRESS)
3. Create detailed task list

EOF
```

#### Step 2: Log the Save
```bash
echo "[$(date)] MEMORY_SAVE: Saved conversation to .memory/conversations/20251107_ecommerce_project.md" >> system_log.md
```

---

## 🎯 Example 2: Saving Decisions

### Scenario
You need to choose between REST API and GraphQL.

### How to Save the Decision

#### Step 1: Create Decision File
```bash
cat > .memory/decisions/api_architecture_20251107.md << 'EOF'
# Decision: REST API vs GraphQL

## Date: 2025-11-07 15:00
## Context: E-commerce platform API design
## Decision Maker: AI Agent (following OSF Framework)

---

## The Question
Should we use REST API or GraphQL for the e-commerce platform?

---

## Options Evaluated

### Option 1: REST API
**Pros:**
- Simpler to implement
- Better caching (HTTP caching)
- Widely understood by developers
- Better tooling (Swagger, Postman)

**Cons:**
- Over-fetching / under-fetching data
- Multiple endpoints for related data
- Versioning can be complex

### Option 2: GraphQL
**Pros:**
- Single endpoint
- Client specifies exact data needed
- Strong typing with schema
- Real-time with subscriptions

**Cons:**
- More complex to implement
- Caching is harder
- Learning curve for team
- Potential for complex queries (performance risk)

---

## OSF Framework Analysis

| Criterion | REST API | GraphQL | Weight |
|-----------|----------|---------|--------|
| **Security** | 8/10 (well-known attack vectors) | 7/10 (query complexity attacks) | 35% |
| **Correctness** | 7/10 (manual validation) | 9/10 (schema validation) | 20% |
| **Reliability** | 9/10 (battle-tested) | 8/10 (newer, but mature) | 15% |
| **Performance** | 8/10 (HTTP caching) | 7/10 (caching is complex) | 10% |
| **Maintainability** | 9/10 (simple, clear) | 7/10 (requires GraphQL knowledge) | 10% |
| **Scalability** | 8/10 (horizontal scaling) | 8/10 (horizontal scaling) | 10% |

**Weighted Score:**
- REST API: (8×0.35) + (7×0.20) + (9×0.15) + (8×0.10) + (9×0.10) + (8×0.10) = **8.15**
- GraphQL: (7×0.35) + (9×0.20) + (8×0.15) + (7×0.10) + (7×0.10) + (8×0.10) = **7.75**

---

## **DECISION: REST API**

## Rationale
REST API scored higher (8.15 vs 7.75) primarily due to:
1. **Security (35% weight):** Better understood, fewer attack vectors
2. **Maintainability (10% weight):** Easier for team to maintain
3. **Performance (10% weight):** Better HTTP caching

While GraphQL has advantages in correctness (schema validation), the security and maintainability benefits of REST API outweigh them for this project.

---

## Implementation Notes
- Use OpenAPI (Swagger) for documentation
- Implement versioning with `/api/v1/` prefix
- Use proper HTTP status codes
- Implement rate limiting per endpoint

---

## Alternatives Considered
- GraphQL: Rejected due to lower OSF score
- gRPC: Not suitable for web clients

---

## Review Date
This decision should be reviewed if:
- Team becomes proficient in GraphQL
- Client explicitly requests GraphQL
- Performance issues arise from over-fetching

EOF
```

#### Step 2: Log the Decision
```bash
echo "[$(date)] DECISION: Chose REST API over GraphQL. OSF score: 8.15 vs 7.75. Saved to .memory/decisions/" >> system_log.md
```

---

## 📸 Example 3: Saving Checkpoints

### Scenario
You've completed Phase 1 (Analysis) and want to save the project state.

### How to Save a Checkpoint

#### Step 1: Create Checkpoint File
```bash
cat > .memory/checkpoints/phase_1_analysis_complete_20251107.md << 'EOF'
# Checkpoint: Phase 1 Analysis Complete

## Date: 2025-11-07 16:00
## Phase: 1 - Analysis
## Status: ✅ COMPLETE

---

## What Was Accomplished

### 1. Project Analysis
- Analyzed existing codebase (if any): N/A (new project)
- Identified requirements: E-commerce platform with 5 core features
- Created project maps: N/A (new project)

### 2. Technology Decisions
- **Frontend:** React + TypeScript
- **Backend:** Node.js + Express
- **Database:** PostgreSQL
- **API:** REST API
- **Payment:** Stripe
- **Email:** SendGrid

### 3. Files Created
- `.memory/conversations/20251107_ecommerce_project.md`
- `.memory/decisions/database_choice_20251107.md`
- `.memory/decisions/api_architecture_20251107.md`
- `docs/requirements.md`

### 4. Key Metrics
- Requirements gathered: 5 core features + 3 additional features
- Decisions made: 6
- Estimated completion time: 4 weeks
- Estimated complexity: Medium-High

---

## Current Project State

### Directory Structure
```
project/
├── .memory/
│   ├── conversations/
│   ├── decisions/
│   └── checkpoints/
├── docs/
│   └── requirements.md
└── system_log.md
```

### Next Phase
**Phase 2: Planning**
- Create detailed task breakdown
- Design database schema
- Design API endpoints
- Create wireframes (if needed)

---

## Blockers / Issues
None at this time.

---

## Notes for Next Session
- User requested email notifications - don't forget to include in planning
- Consider adding admin dashboard to requirements
- Verify Stripe API key availability before implementation

EOF
```

#### Step 2: Log the Checkpoint
```bash
echo "[$(date)] CHECKPOINT: Phase 1 complete. Saved to .memory/checkpoints/phase_1_analysis_complete_20251107.md" >> system_log.md
```

---

## 🧠 Example 4: Maintaining Current Context

### Scenario
You're in the middle of implementing the shopping cart feature.

### How to Save Current Context

#### Step 1: Create/Update Context File
```bash
cat > .memory/context/current_task.md << 'EOF'
# Current Task: Shopping Cart Implementation

## Date: 2025-11-08 10:30
## Phase: 4 - Code Implementation
## Task: Implement shopping cart backend API

---

## What I'm Working On
Implementing the shopping cart API endpoints:
- `POST /api/v1/cart/items` - Add item to cart
- `GET /api/v1/cart` - Get current cart
- `PUT /api/v1/cart/items/:id` - Update item quantity
- `DELETE /api/v1/cart/items/:id` - Remove item from cart

---

## Progress
- [x] Created database schema for cart and cart_items tables
- [x] Implemented POST /api/v1/cart/items
- [x] Implemented GET /api/v1/cart
- [ ] Implementing PUT /api/v1/cart/items/:id (IN PROGRESS)
- [ ] Implementing DELETE /api/v1/cart/items/:id
- [ ] Writing unit tests

---

## Current File
`backend/src/controllers/cart.controller.js`

## Current Function
```javascript
const updateCartItem = async (req, res) => {
  // TODO: Implement quantity update logic
  // TODO: Validate quantity > 0
  // TODO: Check if item exists in cart
  // TODO: Update database
  // TODO: Return updated cart
};
```

---

## Blockers
None

---

## Next Steps
1. Finish updateCartItem function
2. Implement deleteCartItem function
3. Write unit tests for all endpoints
4. Test with Postman
5. Update API documentation

EOF
```

#### Step 2: Update Context Regularly
```bash
# Update context every 30 minutes or when switching tasks
echo "[$(date)] CONTEXT_UPDATE: Updated current task context" >> system_log.md
```

---

## 📚 Example 5: Saving Learnings

### Scenario
You encountered and fixed a tricky bug. Save it for future reference.

### How to Save Learnings

#### Step 1: Create/Update Learnings File
```bash
cat >> .memory/learnings/what_worked_what_didnt.md << 'EOF'

---

## Learning: PostgreSQL Connection Pool Exhaustion

### Date: 2025-11-08 14:00
### Category: Database / Performance

### What Happened
Application started throwing "connection pool exhausted" errors after ~100 concurrent users.

### Root Cause
- Connection pool size was set to default (10)
- Connections were not being properly released after queries
- Missing `client.release()` in error handlers

### What Worked ✅
```javascript
// BEFORE (BAD)
const getUser = async (id) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  } catch (error) {
    throw error; // BUG: client not released!
  } finally {
    client.release(); // This doesn't run if error is thrown
  }
};

// AFTER (GOOD)
const getUser = async (id) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  } catch (error) {
    throw error;
  } finally {
    client.release(); // Always runs
  }
};

// BEST: Use pool.query() directly
const getUser = async (id) => {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
};
```

### Lesson Learned
- Always use `pool.query()` for simple queries
- Only use `client.connect()` when you need transactions
- Always release connections in `finally` block
- Monitor connection pool metrics in production

### Prevention
- Added connection pool monitoring
- Added unit tests for connection release
- Updated all database queries to use `pool.query()`

### Related Files
- `backend/src/config/database.js`
- `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` (also logged there)

EOF
```

---

## 📋 Memory Usage Checklist

At the start of each session:
- [ ] Read `.memory/context/current_task.md` to understand where you left off
- [ ] Read `.memory/checkpoints/` to understand project state
- [ ] Read `.memory/decisions/` to understand past decisions

During work:
- [ ] Save all user interactions to `.memory/conversations/`
- [ ] Save all significant decisions to `.memory/decisions/`
- [ ] Update `.memory/context/current_task.md` every 30 minutes
- [ ] Save learnings to `.memory/learnings/` when you solve problems

At the end of each phase:
- [ ] Create a checkpoint in `.memory/checkpoints/`
- [ ] Update `system_log.md` with checkpoint reference

---

## 🚨 Common Mistakes to Avoid

1. ❌ **Not reading memory before starting** - Always read context first
2. ❌ **Not saving conversations** - Every user interaction must be saved
3. ❌ **Not documenting decisions** - Every significant decision must be documented with OSF analysis
4. ❌ **Not creating checkpoints** - Create a checkpoint at the end of each phase
5. ❌ **Not updating context** - Update current task context regularly

---

## 📚 Related Files

- `prompts/01_memory_management.md` - Memory management prompt
- `prompts/71_memory_save.md` - Memory save prompt
- `system_log.md` - Log all memory operations here
- `errors/DONT_MAKE_THESE_ERRORS_AGAIN.md` - Error memory

---

**Remember: Memory is MANDATORY. Your brain is in `.memory/`. Use it consistently.**

