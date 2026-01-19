# Code Style Rules

## General

- Use 2 spaces for indentation (JavaScript/TypeScript)
- Use 4 spaces for indentation (Python)
- Maximum line length: 100 characters
- Use single quotes for strings (unless interpolation is needed)

## JavaScript/TypeScript

- Use `const` by default, `let` when reassignment is needed
- Never use `var`
- Use arrow functions for callbacks
- Use template literals for string interpolation
- Always use semicolons

## Python

- Follow PEP 8 style guide
- Use type hints for function signatures
- Use docstrings for all public functions and classes
- Use `snake_case` for variables and functions
- Use `PascalCase` for classes

## Enforcement

- Run linter before committing: `npm run lint` or `flake8`
- Use pre-commit hooks to enforce style
