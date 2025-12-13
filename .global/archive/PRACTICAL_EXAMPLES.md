# Practical Examples - Global Guidelines

هذا الملف يحتوي على أمثلة عملية كاملة لاستخدام Global Guidelines في سيناريوهات حقيقية.

---

## Example 1: Complete Bug Fix Workflow

### Scenario
تطبيق ويب يعاني من خطأ في عملية الدفع يؤدي إلى فشل 5% من المعاملات.

### Step-by-Step Execution

#### Phase 1: Detection & Analysis (Automated)

```bash
# 1. Sentry detects error automatically
sentry_event = {
    "error": "PaymentProcessingError: Transaction failed",
    "frequency": "50 occurrences/hour",
    "severity": "high",
    "affected_users": 250,
    "stack_trace": "..."
}

# 2. MCP Integration Layer analyzes context
context = mcp_integration.analyze_context({
    "event_type": "error_detected",
    "source": "sentry",
    "data": sentry_event
})

# Output:
{
    "severity": "high",
    "impact": "critical",  # 5% failure rate
    "urgency": "high",     # Revenue impact
    "priority": "critical",
    "recommended_tools": ["sentry", "code-analysis", "github", "playwright"],
    "estimated_effort": "4-6 hours"
}
```

#### Phase 2: Auto Task Creation

```python
# 3. Task AI creates task automatically
task = task_ai.create_from_template({
    "title": "Fix: Payment processing failure (5% failure rate)",
    "description": """
## Error Details
- Message: PaymentProcessingError: Transaction failed
- Frequency: 50 occurrences/hour
- Affected users: 250
- Revenue impact: $5,000/day

## Stack Trace
{stack_trace}

## Related Issues
- Similar issue fixed in TASK-450
- Payment gateway updated 2 days ago

## Recommended Actions
1. Check payment gateway integration
2. Review recent changes
3. Add comprehensive error handling
4. Improve monitoring
    """,
    "type": "bug",
    "priority": "critical",
    "labels": ["bug", "payment", "critical", "auto-created"],
    "assigned_to": "payment_team_lead@company.com",
    "estimated_effort": "6 hours"
})

# 4. Create GitHub issue
github_issue = github.create_issue({
    "title": task["title"],
    "body": task["description"],
    "labels": task["labels"],
    "assignees": [task["assigned_to"]]
})

# 5. Notify team
slack.send_message({
    "channel": "#critical-bugs",
    "message": f"""
🚨 **Critical Bug Detected**

**Issue:** {task['title']}
**Impact:** 250 users affected, $5,000/day revenue loss
**Assigned to:** @{task['assigned_to']}
**GitHub:** {github_issue['url']}

**Action Required:** Immediate investigation
    """
})
```

#### Phase 3: Investigation (Semi-Automated)

```python
# 6. Gather investigation data
investigation = {
    # Code analysis
    "code_changes": github.get_recent_commits({
        "path": "src/payment/",
        "since": "2 days ago"
    }),
    
    # Similar issues
    "similar_issues": github.search_issues({
        "query": "PaymentProcessingError",
        "state": "closed"
    }),
    
    # Documentation
    "docs": context7.get_documentation({
        "library": "payment-gateway-sdk",
        "version": "current"
    }),
    
    # Error patterns
    "patterns": sentry.analyze_patterns({
        "issue_id": sentry_event["id"],
        "timeframe": "7 days"
    })
}

# 7. Root cause analysis
root_cause = code_analysis.find_root_cause({
    "error": sentry_event,
    "code_changes": investigation["code_changes"],
    "patterns": investigation["patterns"]
})

# Output:
{
    "root_cause": "Payment gateway SDK updated to v2.0, breaking change in error handling",
    "affected_code": "src/payment/gateway.py:145",
    "fix_complexity": "medium",
    "recommended_solution": "Update error handling to match SDK v2.0 API"
}
```

#### Phase 4: Solution Design (Thinking Framework)

```python
# 8. Apply Sequential Thinking
solution = thinking_framework.design_solution({
    "problem": root_cause,
    "context": context,
    "constraints": {
        "time": "must fix within 4 hours",
        "risk": "low - payment is critical",
        "testing": "comprehensive testing required"
    }
})

# Output:
{
    "solutions": [
        {
            "name": "Quick Rollback",
            "approach": "Rollback SDK to v1.x",
            "pros": ["Immediate fix", "Low risk"],
            "cons": ["Temporary solution", "Missing new features"],
            "effort": "30 minutes",
            "recommended": False
        },
        {
            "name": "Proper Fix",
            "approach": "Update error handling for SDK v2.0",
            "pros": ["Permanent solution", "Keeps new features"],
            "cons": ["Takes longer", "Needs testing"],
            "effort": "3 hours",
            "recommended": True
        }
    ],
    "selected": "Proper Fix",
    "implementation_plan": [
        "1. Update error handling code",
        "2. Add comprehensive tests",
        "3. Test in staging",
        "4. Deploy to production",
        "5. Monitor for 24h"
    ]
}
```

#### Phase 5: Implementation (Automated + Manual)

```python
# 9. Create implementation tasks
tasks = task_ai.breakdown_tasks(solution)

# Output:
[
    {
        "id": "TASK-501-1",
        "title": "Update payment gateway error handling",
        "type": "implementation",
        "effort": "2 hours",
        "dependencies": []
    },
    {
        "id": "TASK-501-2",
        "title": "Add comprehensive tests",
        "type": "test",
        "effort": "1 hour",
        "dependencies": ["TASK-501-1"]
    },
    {
        "id": "TASK-501-3",
        "title": "Test in staging environment",
        "type": "test",
        "effort": "30 minutes",
        "dependencies": ["TASK-501-2"]
    },
    {
        "id": "TASK-501-4",
        "title": "Deploy to production",
        "type": "deployment",
        "effort": "30 minutes",
        "dependencies": ["TASK-501-3"]
    }
]

# 10. Developer implements fix (manual)
# ... developer writes code ...

# 11. Auto-run tests
test_results = playwright.test_all({
    "environment": "local",
    "focus": "payment_flow"
})

# 12. Auto-check code quality
quality = ruff.check_project({
    "fix": True,
    "paths": ["src/payment/"]
})
```

#### Phase 6: Deployment (Automated)

```python
# 13. Create PR automatically
pr = github.create_pr({
    "title": "Fix: Payment processing error (SDK v2.0 compatibility)",
    "body": f"""
## Problem
{root_cause['root_cause']}

## Solution
{solution['selected']['approach']}

## Testing
- ✅ Unit tests: {test_results['unit']['passed']}/{test_results['unit']['total']}
- ✅ Integration tests: {test_results['integration']['passed']}/{test_results['integration']['total']}
- ✅ E2E tests: {test_results['e2e']['passed']}/{test_results['e2e']['total']}

## Code Quality
- ✅ Ruff: No issues
- ✅ Test coverage: 95%
- ✅ Security scan: Passed

Closes #{github_issue['number']}
    """,
    "labels": ["bug-fix", "payment", "critical"]
})

# 14. Auto-deploy to staging after PR approval
# (GitHub Actions workflow)

# 15. Run automated tests in staging
staging_tests = playwright.test_all({
    "environment": "staging",
    "comprehensive": True
})

# 16. Deploy to production (after approval)
deployment = cloudflare.deploy({
    "environment": "production",
    "version": pr["merge_commit_sha"]
})

# 17. Monitor post-deployment
monitoring = {
    "sentry": sentry.monitor_issue({
        "issue_id": sentry_event["id"],
        "duration": "24h",
        "alert_if_recurs": True
    }),
    "metrics": cloudflare.get_metrics({
        "metrics": ["error_rate", "response_time", "success_rate"],
        "duration": "24h"
    })
}
```

#### Phase 7: Verification & Learning

```python
# 18. Auto-verify fix
verification = {
    "error_rate": monitoring["metrics"]["error_rate"],  # Should be 0%
    "new_occurrences": monitoring["sentry"]["count"],   # Should be 0
    "user_impact": 0,  # No more affected users
    "revenue_recovered": "$5,000/day"
}

# 19. Learning System records lesson
learning_system.record_lesson({
    "context": {
        "problem_type": "payment_processing_error",
        "root_cause": "sdk_breaking_change",
        "severity": "critical"
    },
    "solution": solution["selected"],
    "outcome": {
        "success": True,
        "time_to_fix": "3.5 hours",
        "quality_score": 95
    },
    "lesson": "Always check SDK changelogs before updating, especially for critical services like payments"
})

# 20. Auto-close tasks and issues
task_ai.complete_task(task["id"])
github.close_issue(github_issue["number"], {
    "comment": f"""
Fixed in PR #{pr['number']}

**Verification:**
- ✅ Error rate: 0%
- ✅ No new occurrences in 24h
- ✅ All tests passing
- ✅ Monitoring shows normal behavior

**Time to Resolution:** 3.5 hours
**Impact:** $5,000/day revenue recovered, 250 users no longer affected
    """
})

# 21. Send success notification
slack.send_message({
    "channel": "#critical-bugs",
    "message": """
✅ **Bug Fixed Successfully**

**Issue:** Payment processing failure
**Resolution Time:** 3.5 hours
**Impact:** $5,000/day revenue recovered

**Verification:**
- Error rate: 0%
- 24h monitoring: No issues
- All tests passing

Great work team! 🎉
    """
})
```

### Summary

**Total Time:** 3.5 hours (vs 8-12 hours manual)
**Automation Level:** 85%
**Manual Steps:** Code implementation, PR review, production deployment approval
**Automated Steps:** Detection, analysis, task creation, testing, monitoring, documentation, learning

---

## Example 2: New Feature Development

### Scenario
إضافة ميزة "Dark Mode" لتطبيق ويب.

### Complete Workflow

```python
# 1. Feature request received
feature_request = {
    "title": "Add Dark Mode",
    "description": "Users want dark mode option",
    "requested_by": "product_manager",
    "user_votes": 450,
    "business_value": "high"
}

# 2. MCP Integration analyzes and creates tasks
analysis = mcp_integration.analyze_feature_request(feature_request)

# Output:
{
    "complexity": "medium",
    "estimated_effort": "40 hours",
    "required_skills": ["frontend", "design", "testing"],
    "dependencies": [],
    "priority": "high",  # Based on user votes
    "recommended_approach": "CSS variables + localStorage",
    "tasks": [
        {
            "phase": "Design",
            "tasks": [
                "Design dark mode color palette",
                "Create design mockups",
                "Get stakeholder approval"
            ],
            "effort": "8 hours"
        },
        {
            "phase": "Implementation",
            "tasks": [
                "Setup CSS variables",
                "Implement theme toggle",
                "Update all components",
                "Add localStorage persistence"
            ],
            "effort": "20 hours"
        },
        {
            "phase": "Testing",
            "tasks": [
                "Write unit tests",
                "Write E2E tests",
                "Manual QA testing",
                "Accessibility testing"
            ],
            "effort": "8 hours"
        },
        {
            "phase": "Documentation",
            "tasks": [
                "Update user documentation",
                "Update developer documentation"
            ],
            "effort": "4 hours"
        }
    ]
}

# 3. Auto-create all tasks
for phase in analysis["tasks"]:
    for task_title in phase["tasks"]:
        task_ai.create_task({
            "title": task_title,
            "phase": phase["phase"],
            "estimated_effort": phase["effort"] / len(phase["tasks"]),
            "labels": ["feature", "dark-mode", phase["phase"].lower()]
        })

# 4. Auto-generate project structure map
project_map = mcp_integration.generate_project_map({
    "feature": "dark_mode",
    "affected_components": [
        "src/styles/",
        "src/components/",
        "src/hooks/",
        "src/utils/"
    ]
})

# 5. Implementation with continuous quality checks
# ... developer implements ...

# 6. Auto-run quality checks on each commit
on_commit = {
    "ruff": ruff.check_project({"fix": True}),
    "eslint": eslint.lint_directory({"fix": True}),
    "tests": playwright.test_all(),
    "accessibility": playwright.test_accessibility()
}

# 7. Auto-deployment pipeline
# ... same as bug fix example ...

# 8. Learning system records successful feature
learning_system.record_success({
    "feature_type": "ui_enhancement",
    "approach": "css_variables",
    "effort_estimated": "40 hours",
    "effort_actual": "38 hours",
    "quality_score": 92,
    "user_satisfaction": 4.8
})
```

---

## Example 3: Code Quality Improvement

### Scenario
تحسين جودة الكود بشكل مستمر.

### Daily Automated Workflow

```python
# Runs automatically every day at 2 AM

# 1. Comprehensive code analysis
analysis = {
    "python": ruff.check_project(),
    "javascript": eslint.lint_directory(),
    "security": code_analysis.security_scan(),
    "complexity": code_analysis.measure_complexity(),
    "dead_code": code_analysis.find_dead_code(),
    "test_coverage": pytest.get_coverage()
}

# 2. Auto-fix what can be fixed
auto_fixed = {
    "python": ruff.fix_issues(analysis["python"]["auto_fixable"]),
    "javascript": eslint.fix_issues(analysis["javascript"]["auto_fixable"])
}

# 3. Create tasks for manual fixes
manual_issues = [
    issue for category in analysis.values()
    for issue in category.get("manual_fixes_needed", [])
]

for issue in manual_issues:
    task_ai.create_task({
        "title": f"Fix: {issue['description']}",
        "type": "code_quality",
        "priority": issue["severity"],
        "file": issue["file"],
        "line": issue["line"]
    })

# 4. Create PR for auto-fixes
if auto_fixed["python"] or auto_fixed["javascript"]:
    pr = github.create_pr({
        "title": "Auto-fix: Daily code quality improvements",
        "body": format_auto_fixes(auto_fixed),
        "labels": ["auto-fix", "code-quality"]
    })

# 5. Generate quality report
report = generate_quality_report(analysis)
slack.send_message({
    "channel": "#code-quality",
    "message": report
})

# 6. Track trends
learning_system.record_quality_metrics({
    "date": datetime.now(),
    "metrics": {
        "code_quality_score": calculate_score(analysis),
        "test_coverage": analysis["test_coverage"]["percentage"],
        "security_issues": len(analysis["security"]["issues"]),
        "complexity": analysis["complexity"]["average"]
    }
})
```

---

## Key Takeaways

### Automation Benefits

1. **Speed:** 80-90% faster than manual process
2. **Consistency:** Same quality every time
3. **Coverage:** Nothing is missed
4. **Learning:** Continuous improvement
5. **Documentation:** Automatic and complete

### Human Role

1. **Code Implementation:** Write the actual code
2. **Design Decisions:** Make architectural choices
3. **PR Review:** Review and approve changes
4. **Production Deployment:** Final approval for critical deployments
5. **Strategic Planning:** Long-term planning and direction

### Best Practices

1. **Trust the System:** Let automation handle routine tasks
2. **Review Decisions:** Always review automated decisions
3. **Provide Feedback:** Help the learning system improve
4. **Monitor Results:** Track automation effectiveness
5. **Iterate:** Continuously improve the automation

---

## Next Steps

1. **Apply to Your Project:** Use these examples as templates
2. **Customize:** Adapt to your specific needs
3. **Measure:** Track the impact
4. **Learn:** Improve based on results
5. **Share:** Share your learnings with the team

