# Naming Conventions

## Variables

- Use descriptive names: `userEmail` not `ue`
- Use camelCase for JavaScript/TypeScript
- Use snake_case for Python
- Boolean variables should start with `is`, `has`, `should`: `isActive`, `hasPermission`

## Functions

- Use verb-noun pattern: `getUserById`, `createOrder`, `deleteComment`
- Use camelCase for JavaScript/TypeScript
- Use snake_case for Python

## Classes

- Use PascalCase: `UserController`, `OrderService`
- Use singular nouns: `User` not `Users`

## Constants

- Use UPPER_SNAKE_CASE: `MAX_RETRIES`, `API_BASE_URL`

## Files

- Use kebab-case for file names: `user-controller.js`, `order-service.py`
- Match file name to main export: `UserController` class in `user-controller.js`
