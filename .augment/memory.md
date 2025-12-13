# 🧠 Memory Management Rules

## Purpose

Memory management ensures context retention across interactions. Without it, you forget important decisions and repeat work.

---

## ⚡ Mandatory Activation

**ALWAYS activate memory management at the START of EVERY task!**

This is NOT optional. This is REQUIRED.

---

## 📋 When to Use Memory

### **Always:**
1. **At task start** - Initialize memory system
2. **When user provides information** - Save requirements
3. **When making decisions** - Document choices
4. **When discovering issues** - Record problems
5. **When completing milestones** - Save progress
6. **Throughout the task** - Continuous updates

---

## 🔧 How to Use Memory

### **1. Initialize**
```
At the very start:
- Create memory context
- Load previous context if exists
- Prepare memory structure
```

### **2. Save Context**
```
Save these to memory:
- Project requirements
- User preferences
- Technical decisions
- Architecture choices
- Known issues
- Completed tasks
- Next steps
```

### **3. Retrieve Context**
```
Before making decisions:
- Check what was decided before
- Review previous issues
- Understand current state
- Avoid repeating work
```

### **4. Update Memory**
```
As project evolves:
- Update status
- Add new information
- Mark completed items
- Document changes
```

---

## 📝 What to Save

### **Project Information**
- Project name and purpose
- Technology stack
- Architecture decisions
- File structure

### **Requirements**
- Functional requirements
- Non-functional requirements
- Constraints
- Success criteria

### **Decisions**
- Why this approach?
- What alternatives were considered?
- What are the trade-offs?

### **Progress**
- What's completed?
- What's in progress?
- What's pending?
- What's blocked?

### **Issues**
- Known bugs
- Technical debt
- Workarounds
- Future improvements

### **Dependencies**
- External libraries
- APIs used
- Services integrated
- Version requirements

---

## 🎯 Memory Structure

### **Recommended Format:**
```json
{
  "project": {
    "name": "Project Name",
    "type": "web_app",
    "stack": ["Python", "Django", "PostgreSQL"],
    "status": "in_progress"
  },
  "requirements": {
    "functional": [...],
    "non_functional": [...]
  },
  "architecture": {
    "pattern": "MVC",
    "components": [...],
    "decisions": [...]
  },
  "progress": {
    "completed": [...],
    "in_progress": [...],
    "pending": [...]
  },
  "issues": {
    "bugs": [...],
    "technical_debt": [...],
    "improvements": [...]
  },
  "dependencies": {
    "backend": [...],
    "frontend": [...],
    "database": [...]
  }
}
```

---

## ⚠️ Critical Rules

### **DO:**
- ✅ Initialize memory at task start
- ✅ Save important information immediately
- ✅ Update memory continuously
- ✅ Retrieve context before decisions
- ✅ Document why, not just what
- ✅ Keep memory structured and organized

### **DON'T:**
- ❌ Skip memory initialization
- ❌ Rely only on conversation context
- ❌ Forget to update memory
- ❌ Save unimportant details
- ❌ Create messy, unstructured memory
- ❌ Ignore previous context

---

## 🔄 Memory Lifecycle

### **Phase 1: Initialize**
```
Task Start
    ↓
Initialize Memory
    ↓
Load Previous Context (if exists)
    ↓
Ready to Work
```

### **Phase 2: Active Use**
```
Work on Task
    ↓
Make Decision → Save to Memory
    ↓
Discover Issue → Save to Memory
    ↓
Complete Milestone → Save to Memory
    ↓
Continue Working
```

### **Phase 3: Handoff**
```
Complete Phase
    ↓
Update Memory with Results
    ↓
Document Next Steps
    ↓
Pass to Next Expert
```

### **Phase 4: Final**
```
Task Complete
    ↓
Final Memory Update
    ↓
Create Summary
    ↓
Save for Future Reference
```

---

## 💡 Best Practices

### **1. Be Specific**
```
❌ Bad:  "User wants a website"
✅ Good: "User wants an e-commerce website with:
         - Product catalog
         - Shopping cart
         - Payment integration (Stripe)
         - Admin dashboard
         - Mobile responsive"
```

### **2. Document Decisions**
```
❌ Bad:  "Using PostgreSQL"
✅ Good: "Using PostgreSQL because:
         - Complex relationships needed
         - ACID compliance required
         - Team has expertise
         - Better than MongoDB for this use case"
```

### **3. Track Progress**
```
❌ Bad:  "Working on backend"
✅ Good: "Backend Progress:
         ✅ User authentication (completed)
         🔄 Product API (in progress - 60%)
         ⏳ Order processing (pending)
         ❌ Payment integration (blocked - need API keys)"
```

### **4. Record Issues**
```
❌ Bad:  "There's a bug"
✅ Good: "Bug: Login fails with special characters
         - Error: 'Invalid credentials'
         - Cause: Password validation regex too strict
         - Impact: Users can't login with complex passwords
         - Fix: Update regex pattern
         - Status: Fixed in commit abc123"
```

---

## 🎓 Examples

### **Example 1: E-commerce Project**
```json
{
  "project": {
    "name": "ShopEasy",
    "type": "e-commerce",
    "stack": ["Django", "React", "PostgreSQL", "Redis"],
    "status": "development"
  },
  "requirements": {
    "functional": [
      "User registration and authentication",
      "Product browsing and search",
      "Shopping cart",
      "Checkout with Stripe",
      "Order tracking",
      "Admin dashboard"
    ],
    "non_functional": [
      "Response time < 200ms",
      "Support 10,000 concurrent users",
      "99.9% uptime",
      "Mobile responsive"
    ]
  },
  "architecture": {
    "pattern": "Microservices",
    "components": [
      "User Service (Django)",
      "Product Service (Django)",
      "Order Service (Django)",
      "Payment Service (Stripe Integration)",
      "Frontend (React SPA)",
      "API Gateway (Kong)"
    ]
  },
  "progress": {
    "completed": [
      "User authentication",
      "Product catalog",
      "Shopping cart"
    ],
    "in_progress": [
      "Checkout flow (70%)",
      "Admin dashboard (40%)"
    ],
    "pending": [
      "Order tracking",
      "Email notifications",
      "Analytics"
    ]
  }
}
```

### **Example 2: API Development**
```json
{
  "project": {
    "name": "WeatherAPI",
    "type": "rest_api",
    "stack": ["FastAPI", "PostgreSQL", "Redis"],
    "status": "testing"
  },
  "decisions": [
    {
      "decision": "Use FastAPI instead of Flask",
      "reason": "Need async support and automatic API docs",
      "date": "2025-11-01"
    },
    {
      "decision": "Cache responses in Redis",
      "reason": "Weather data changes slowly, reduce API calls",
      "ttl": "5 minutes"
    }
  ],
  "issues": [
    {
      "type": "bug",
      "description": "Rate limiting not working",
      "status": "fixed",
      "solution": "Updated Redis key format"
    }
  ]
}
```

---

## 🚀 Quick Start

**For every task:**

1. **Initialize Memory**
   ```
   "I'm initializing memory management for this task..."
   ```

2. **Save Initial Context**
   ```
   Project: [name]
   Type: [type]
   Requirements: [list]
   ```

3. **Update Continuously**
   ```
   As you work, save:
   - Decisions made
   - Issues found
   - Progress achieved
   ```

4. **Final Update**
   ```
   Before completing:
   - Summary of work
   - What's done
   - What's next
   ```

---

## ⚡ Remember

**Memory is NOT optional!**

Without memory:
- ❌ You forget decisions
- ❌ You repeat work
- ❌ You lose context
- ❌ You make inconsistent choices

With memory:
- ✅ You remember everything
- ✅ You build on previous work
- ✅ You maintain context
- ✅ You make consistent decisions

**Always use memory. Always.**

---

*Memory management is your foundation. Build on it, and you'll never forget.*

