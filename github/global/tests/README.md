# Tests — Global System v26.0.2 Diamond 32

> Test suite for system verification.

## Running Tests
```bash
make test          # Run all tests
make test-cov      # Run with coverage
pytest tests/ -v   # Verbose output
```

## Test Files
- `conftest.py` — Shared fixtures
- `test_placeholder.py` — Placeholder tests
- `test_gap_analysis.py` — Gap analysis verification
- `test_verify_remediation.py` — Remediation verification
- `e2e/test_user_flow.py` — End-to-end user flow tests
