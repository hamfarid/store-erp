---
type: manual
description: Complete project lifecycle workflow
---

# Full Project Workflow

## When to Use

Use this workflow when:
- ✅ Starting a complete new project from scratch
- ✅ Building entire application (not just a feature)
- ✅ Project will take days/weeks
- ✅ Multiple components and integrations

Don't use when:
- ❌ Adding single feature to existing project
- ❌ Quick prototype or POC
- ❌ Bug fix or maintenance

## Complete Workflow

### Phase 0: PREPARATION

```
1. Read CORE_PROMPT_v10.md (understand who you are)
2. Verify environment separation
3. Initialize Memory + MCP
4. Save initialization to memory
```

### Phase 1: INITIALIZE PROJECT

```
1. Get project information
   - Project name?
   - Project type?
   - Requirements?
   - Technologies?
   - Timeline?
   
2. Create project structure
   📂 ~/user-project/.ai/     (tracking files)
   📂 ~/user-project/src/     (code)
   📂 ~/user-project/tests/   (tests)
   📂 ~/user-project/docs/    (documentation)
   
3. Copy templates from knowledge/templates/
   - PROJECT_PLAN.md
   - PROGRESS_TRACKER.md
   - DECISIONS_LOG.md
   - ARCHITECTURE.md
   
4. Initialize version control
   - git init
   - .gitignore
   - Initial commit
   
5. Save project context to memory
```

### Phase 2: PLANNING

```
1. Understand requirements
   - Core features?
   - Constraints?
   - Success criteria?
   - Save to memory
   - Document in .ai/PROJECT_PLAN.md
   
2. Design architecture
   - What components?
   - What technologies?
   - Choose BEST, not easiest!
   
3. For each technology choice:
   - Evaluate options
   - Choose best fit
   - Document rationale
   - Log alternatives
   - Note trade-offs
   - Save to memory
   - Log in .ai/DECISIONS_LOG.md
   
4. Create detailed plan
   - Break into phases (3-5)
   - Define tasks per phase
   - Estimate effort
   - Set success criteria
   - Document in .ai/PROJECT_PLAN.md
   - Save to memory
   
5. Review with user
   - Present plan
   - Get approval
   - Update based on feedback
   - Save approved plan to memory
```

### Phase 3: BUILD

```
For each development phase:

1. Set up phase
   - Update .ai/PROGRESS_TRACKER.md
   - Save phase start to memory
   
2. Implement features
   - Read relevant knowledge items
   - Implement with best practices
   - Test thoroughly
   - Document code
   - Update progress tracker
   - Save milestones to memory
   
3. Test continuously
   - Run unit tests
   - Run integration tests
   - Coverage >= 95%?
   
4. Document as you go
   - Code comments
   - API documentation
   - README files
   - Update .ai/ARCHITECTURE.md
   
5. Log decisions
   - Log in .ai/DECISIONS_LOG.md
   - Save to memory
   
6. Quality gate
   [ ] All tests passing?
   [ ] Coverage >= 95%?
   [ ] No critical issues?
   [ ] Code reviewed?
   [ ] Documentation updated?
   
7. Save phase completion to memory
8. Update .ai/PROGRESS_TRACKER.md
```

### Phase 4: FINALIZE

```
1. Complete testing
   - All unit tests
   - All integration tests
   - End-to-end tests
   - Security scan
   - Performance test
   
2. Finalize documentation
   - README.md
   - INSTALL.md
   - API.md
   - DEPLOYMENT.md
   - TROUBLESHOOTING.md
   
3. Prepare deployment
   - Deployment checklist
   - Test deployment scripts
   - Document rollback plan
   
4. Create handoff document
   - Copy knowledge/templates/HANDOFF.md
   - Fill with project details
   - Include key decisions
   - Document how to run/deploy
   - Save to .ai/HANDOFF.md
```

### Phase 5: DELIVER

```
1. Deploy to production
   - Run deployment
   - Verify deployment
   - Monitor for issues
   - Save deployment to memory
   
2. Verify functionality
   [ ] Application accessible?
   [ ] All features working?
   [ ] No errors in logs?
   [ ] Performance acceptable?
   [ ] Security headers present?
   
3. Archive project context
   - Save complete context to memory:
     * Project summary
     * Key decisions
     * Challenges faced
     * Solutions implemented
     * Learnings
     * Recommendations
   
4. Deliver to user
   - Working application (deployed)
   - Source code (repository)
   - Documentation (complete)
   - Handoff document
   - Access credentials (if applicable)
```

## Quality Gates

### Code Quality
- Follows best practices
- Clean and readable
- Well-documented
- No code smells
- Passes linting

### Testing Quality
- 95%+ coverage
- All tests passing
- Edge cases covered
- Performance tested
- Security tested

### Documentation Quality
- Complete and accurate
- Clear and concise
- Examples provided
- Up to date
- Easy to follow

### Architecture Quality
- Scalable design
- Maintainable code
- Security considered
- Performance optimized
- Best solution chosen (not easiest!)

## Remember

- Initialize Memory + MCP first
- Verify environment separation
- Choose best solutions
- Document everything
- Test thoroughly
- Deliver quality

