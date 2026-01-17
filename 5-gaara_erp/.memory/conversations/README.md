# 💬 Conversations Memory

> **Purpose:** Store and organize all conversations for context and learning.

**Version:** 2.0  
**Last Updated:** November 7, 2025  
**Total Conversations:** 0

---

## 📁 Structure

```
conversations/
├── README.md                    # This file
├── index.json                   # Conversation index
├── daily/                       # Daily conversations
│   └── 2025-11-07_database_design.md
├── weekly/                      # Weekly summaries
│   └── 2025-W45_summary.md
├── monthly/                     # Monthly summaries
│   └── 2025-11_summary.md
└── important/                   # Important conversations
    └── architecture_decisions.md
```

---

## 📝 Conversation Template

```markdown
# Conversation: [Topic]

**Date:** YYYY-MM-DD HH:MM:SS  
**Session ID:** sess_YYYYMMDD_HHMMSS  
**Duration:** X minutes  
**Participants:** User, Lead Agent, Reviewer Agent

---

## 📋 Context

**Project:** [Project Name]  
**Phase:** [Planning/Implementation/Testing/Deployment]  
**Current Task:** [Task Description]  
**Previous Context:** [Link to previous conversation]

---

## 💬 Conversation

### User (10:00:00)
[User message]

### Lead Agent (10:00:15)
[Agent response]

### User (10:01:00)
[User message]

### Lead Agent (10:01:30)
[Agent response]

---

## 🎯 Outcomes

**Decisions Made:**
1. [Decision 1]
2. [Decision 2]

**Tasks Created:**
- [ ] [Task 1]
- [ ] [Task 2]

**Knowledge Gained:**
- [Knowledge 1]
- [Knowledge 2]

**Files Modified:**
- `src/file1.py`
- `src/file2.py`

**Next Steps:**
1. [Step 1]
2. [Step 2]

---

## 🔗 Related

**Previous:** [Link]  
**Next:** [Link]  
**Related Conversations:** [Links]  
**Related Knowledge:** [Links]

---

## 📊 Metadata

**Tags:** #database #design #postgresql  
**Priority:** High  
**Status:** Complete  
**Saved To Memory:** ✅  
**Indexed:** ✅
```

---

## 🔍 How to Search

### By Date
```bash
find conversations/daily -name "2025-11-07*.md"
```

### By Topic
```bash
grep -r "database design" conversations/
```

### By Tag
```bash
grep -r "#database" conversations/
```

---

## 📊 Statistics

**This Week:**
- Conversations: 0
- Average duration: 0 min
- Topics covered: 0

**This Month:**
- Conversations: 0
- Most discussed topic: N/A
- Knowledge items created: 0

---

💬 **Every conversation is valuable. Save it, learn from it!** 💬

