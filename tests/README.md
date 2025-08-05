# LP Optimizer Tests

This directory contains all tests for the Linear Programming Optimizer application.

## Test Files

- `test_solvers.py` - Comprehensive unit tests for both PuLP and HiGHS solvers
- `test_highs.py` - Specific test for HiGHS solver implementation with the example problem
- `test_both_solvers.py` - Comparison tests between PuLP and HiGHS solvers
- `test_app_integration.py` - Integration tests for the Dash application

## Running Tests

### Run all tests:
```bash
uv run python -m pytest tests/
```

### Run specific test file:
```bash
uv run python tests/test_solvers.py
```

### Run with verbose output:
```bash
uv run python -m pytest tests/ -v
```

## Test Coverage

The test suite covers:
- Basic maximization and minimization problems
- Infeasible and unbounded problems
- Equality constraints
- Negative coefficients
- Multiple variables (3+ dimensions)
- Error handling for malformed inputs
- Solver consistency between PuLP and HiGHS
- App integration and callback functionality