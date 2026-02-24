# Code Review Workflow (v26.0.2 Diamond 32)

## Purpose
Standardized peer review process ensuring code quality, security, and maintainability.

## Trigger
- Pull request opened or updated
- Manual review request via team lead

## Steps

### 1. Pre-Review Checklist
- Confirm PR description explains the change
- Verify linked issue/task reference
- Check CI pipeline passed (lint, tests, build)

### 2. Code Review
- **Architecture**: Does the change fit the existing patterns?
- **Security**: No secrets, no SQL injection, input validated
- **Performance**: No N+1 queries, no unnecessary loops
- **Readability**: Clear naming, proper comments on complex logic
- **Tests**: New code has corresponding tests

### 3. Feedback
- Use inline comments for specific issues
- Classify as: blocking, suggestion, or question
- Provide code examples for suggested improvements

### 4. Resolution
- Author addresses all blocking comments
- Reviewer re-reviews changes
- Approve only when all blocking items resolved

### 5. Post-Merge
- Delete feature branch
- Verify deployment pipeline triggered
- Update task status in project tracker

## Roles
- **Author**: Developer who wrote the code
- **Reviewer**: Peer developer (minimum 1, recommended 2)
- **Approver**: Team lead for critical paths

## Templates
- `templates/code_review_checklist.md` — Review checklist
- `templates/pr_template.md` — Pull request template
