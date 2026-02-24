 (v15.9.8)
**Verified Feb 2026 Standard**

## Scenario: Implement a Login Function

### 1. Write the Eval (First!)
Create `tests/evals/login.yaml`:
```yaml
prompts: [ "Login with user={{user}} pass={{pass}}" ]
providers: [ "python:app.auth.login" ]
tests:
  - vars:
      user: "admin"
      pass: "correct_password"
    assert:
      - type: contains
        value: "token"
  - vars:
      user: "admin"
      pass: "wrong_password"
    assert:
      - type: contains
        value: "error"
```

### 2. Run the Eval (It Fails)
```bash
npx promptfoo eval -c tests/evals/login.yaml
# Result: ❌ FAILED (Function not implemented)
```

### 3. Implement the Code
```python
def login(user, password):
    if user == "admin" and password == "correct_password":
        return {"token": "xyz"}
    return {"error": "Invalid credentials"}
```

### 4. Run the Eval (It Passes)
```bash
npx promptfoo eval -c tests/evals/login.yaml
# Result: ✅ PASSED (Score: 1.0)
```
