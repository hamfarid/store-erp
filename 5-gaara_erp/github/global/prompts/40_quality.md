# CODE QUALITY REVIEW PROMPT

**FILE**: github/global/prompts/40_quality.md | **PURPOSE**: Automated code quality review | **OWNER**: System | **LAST-AUDITED**: 2025-11-18

## Phase 5: Review & Refinement - Quality

This prompt guides you through automated code quality review and improvement.

## Pre-Execution Checklist

- [ ] Code implementation complete
- [ ] Linting tools installed
- [ ] Code formatters configured

## Quality Checks

### 1. Linting

#### Python (Flake8, Pylint, mypy)

```bash
# Install tools
pip install flake8 pylint mypy black isort

# Run linting
flake8 backend/ --max-line-length=120 --exclude=venv,__pycache__
pylint backend/ --max-line-length=120
mypy backend/ --strict

# Auto-format
black backend/
isort backend/
```

#### JavaScript/TypeScript (ESLint, Prettier)

```bash
# Install tools
npm install --save-dev eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Run linting
npx eslint frontend/src/ --ext .ts,.tsx
npx prettier --check frontend/src/

# Auto-format
npx eslint frontend/src/ --ext .ts,.tsx --fix
npx prettier --write frontend/src/
```

### 2. Code Complexity

Check cyclomatic complexity (should be <10):

```bash
# Python
pip install radon
radon cc backend/ -a -nb

# JavaScript/TypeScript
npm install -g complexity-report
cr frontend/src/ --format json
```

### 3. Code Duplication

Detect duplicate code (should be <5%):

```bash
# Python
pip install pylint
pylint --disable=all --enable=duplicate-code backend/

# JavaScript/TypeScript
npm install -g jscpd
jscpd frontend/src/
```

### 4. Type Coverage

Ensure strong typing:

```bash
# Python
mypy backend/ --strict --html-report mypy-report

# TypeScript
npx tsc --noEmit --strict
```

### 5. Documentation Coverage

Check docstring coverage:

```bash
# Python
pip install interrogate
interrogate backend/ -v --fail-under=80

# JavaScript/TypeScript (JSDoc)
npm install -g documentation
documentation lint frontend/src/**/*.ts
```

### 6. Code Style Consistency

Enforce consistent code style:

```bash
# Python
black --check backend/
isort --check-only backend/

# JavaScript/TypeScript
prettier --check frontend/src/
```

## Quality Metrics

### Target Metrics

- **Linting Errors**: 0
- **Type Coverage**: 100%
- **Cyclomatic Complexity**: <10 per function
- **Code Duplication**: <5%
- **Documentation Coverage**: >80%
- **Line Length**: <120 characters
- **Function Length**: <50 lines
- **File Length**: <500 lines

## Automated Fixes

### Python

```bash
# Auto-fix imports
isort backend/

# Auto-format code
black backend/

# Remove unused imports
autoflake --remove-all-unused-imports --in-place --recursive backend/
```

### JavaScript/TypeScript

```bash
# Auto-fix linting issues
npx eslint frontend/src/ --ext .ts,.tsx --fix

# Auto-format code
npx prettier --write frontend/src/

# Remove unused imports
npx ts-prune
```

## Code Review Checklist

### General

- [ ] No hardcoded values (use constants/config)
- [ ] No commented-out code
- [ ] No TODO comments without owner and date
- [ ] No console.log/print statements (use proper logging)
- [ ] No magic numbers (use named constants)

### Functions

- [ ] Single responsibility
- [ ] Max 50 lines
- [ ] Max 3 parameters (use objects for more)
- [ ] Descriptive names (verb + noun)
- [ ] Proper error handling
- [ ] Documented with docstring/JSDoc

### Classes

- [ ] Single responsibility
- [ ] Proper encapsulation (private/public)
- [ ] Documented with docstring/JSDoc
- [ ] No god classes (>500 lines)

### Files

- [ ] Single purpose
- [ ] Proper header comment
- [ ] Organized imports
- [ ] Max 500 lines

### Naming

- [ ] Variables: camelCase (JS/TS), snake_case (Python)
- [ ] Functions: camelCase (JS/TS), snake_case (Python)
- [ ] Classes: PascalCase
- [ ] Constants: UPPER_SNAKE_CASE
- [ ] Files: kebab-case.ts, snake_case.py

## Quality Report

Create `docs/QUALITY_REPORT.md`:

```markdown
# Code Quality Report

**Generated**: [Date]

## Summary

- **Linting Errors**: [Count]
- **Type Errors**: [Count]
- **Complexity Issues**: [Count]
- **Duplication**: [Percentage]
- **Documentation Coverage**: [Percentage]

## Linting Issues

### Critical (P0)
1. **File**: `backend/services/auth.py`
   - **Line**: 45
   - **Issue**: Undefined variable 'user'
   - **Fix**: Define variable before use

[Repeat for all issues]

## Complexity Issues

### Functions with High Complexity (>10)
1. **Function**: `process_payment`
   - **File**: `backend/services/payment.py`
   - **Complexity**: 15
   - **Recommendation**: Break into smaller functions

## Code Duplication

### Duplicate Blocks
1. **Files**: `backend/services/user.py` and `backend/services/admin.py`
   - **Lines**: 45-60 and 78-93
   - **Recommendation**: Extract to shared utility function

## Documentation Gaps

### Undocumented Functions
1. `backend/services/auth.py::login` - Missing docstring
2. `frontend/src/services/api.ts::refreshToken` - Missing JSDoc

## Recommendations

1. Fix all linting errors (P0)
2. Reduce complexity in identified functions (P1)
3. Remove code duplication (P1)
4. Add missing documentation (P2)

---

**Next Steps**: Address all P0 and P1 issues
```

## CI Integration

Add quality checks to CI pipeline:

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install Python tools
        run: |
          pip install flake8 pylint mypy black isort
      
      - name: Run Python linting
        run: |
          flake8 backend/ --max-line-length=120
          pylint backend/ --max-line-length=120
          mypy backend/ --strict
      
      - name: Check Python formatting
        run: |
          black --check backend/
          isort --check-only backend/
      
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Install Node.js tools
        run: |
          npm install
      
      - name: Run TypeScript linting
        run: |
          npx eslint frontend/src/ --ext .ts,.tsx
          npx prettier --check frontend/src/
      
      - name: Run TypeScript type checking
        run: |
          npx tsc --noEmit --strict
```

## Log Actions

Log all quality findings to `logs/info.log`

## Save to Memory

Save quality report to `.memory/learnings/quality_review_[date].md`

---

**Completion Criteria**:
- [ ] All linting errors fixed
- [ ] All type errors fixed
- [ ] Complexity reduced to acceptable levels
- [ ] Code duplication removed
- [ ] Documentation coverage ≥80%
- [ ] Quality report generated
- [ ] CI checks passing
- [ ] Actions logged

