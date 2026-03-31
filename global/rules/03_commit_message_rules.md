# Commit Message Rules

Follow the Conventional Commits specification.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build config)

## Examples

```
feat(auth): add JWT refresh token support

Implement refresh token rotation to improve security.
Users can now refresh their access tokens without re-authenticating.

Closes #123
```

```
fix(api): handle null values in user profile endpoint

Previously, the API would crash if a user had no profile picture.
Now it returns a default placeholder image.
```

## Rules

- Use imperative mood: "add feature" not "added feature"
- Keep subject line under 50 characters
- Capitalize the subject line
- Do not end subject line with a period
- Separate subject from body with a blank line
