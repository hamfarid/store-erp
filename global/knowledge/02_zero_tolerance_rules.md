# Zero Tolerance Rules

> **These rules MUST NEVER be violated. No exceptions.**

**Version:** 1.0
**Last Updated:** 2025-01-16

---

## ❌ The 10 Non-Negotiable Rules

### 1. No Hardcoded Secrets
```python
# ❌ NEVER
SECRET_KEY = "my-secret-key-123"

# ✅ ALWAYS
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 2. No SQL Injection
```python
# ❌ NEVER
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ ALWAYS
query = "SELECT * FROM users WHERE id = :id"
db.execute(query, {'id': user_id})
```

### 3. No XSS Vulnerabilities
```jsx
// ❌ NEVER
<div dangerouslySetInnerHTML={{__html: userContent}} />

// ✅ ALWAYS
<div>{userContent}</div>
```

### 4. No Unhandled Errors
```python
# ❌ NEVER
data = json.loads(request.data)

# ✅ ALWAYS
try:
    data = json.loads(request.data)
except json.JSONDecodeError as e:
    logger.error(f"JSON parse error: {e}")
    return {"error": "Invalid JSON"}, 400
```

### 5. No Missing Tests (80%+ Coverage Required)
```bash
# Check coverage before commit
pytest --cov=src --cov-fail-under=80
```

### 6. No Undocumented Code
```python
# ❌ NEVER
def process(x, y):
    return x * y + 0.1

# ✅ ALWAYS
def calculate_total_with_tax(subtotal: float, tax_rate: float) -> float:
    """
    Calculate total price including tax.
    
    Args:
        subtotal: Price before tax
        tax_rate: Tax rate as decimal (e.g., 0.1 for 10%)
        
    Returns:
        Total price including tax
    """
    return subtotal * (1 + tax_rate)
```

### 7. No Duplicate Code (DRY Principle)
```python
# ❌ NEVER (copy-paste code)
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# ✅ ALWAYS (use helper)
def get_user_by(**kwargs):
    return User.query.filter_by(**kwargs).first()
```

### 8. No Uncommitted Changes
```bash
# Commit frequently with meaningful messages
git add .
git commit -m "feat(products): add lot expiry tracking"
```

### 9. No Direct DOM Manipulation (Frontend)
```jsx
// ❌ NEVER
document.getElementById('price').innerText = newPrice;

// ✅ ALWAYS
const [price, setPrice] = useState(0);
setPrice(newPrice);
// <span>{price}</span>
```

### 10. No Bypassing Validation
```python
# ❌ NEVER (direct access)
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()

# ✅ ALWAYS (validate first)
@app.route('/api/users/<int:id>', methods=['DELETE'])
@require_permission('user.delete')
def delete_user(id):
    user = User.query.get_or_404(id)
    if not current_user.can_delete(user):
        return {"error": "Forbidden"}, 403
    db.session.delete(user)
```

---

## 🚨 Consequences of Violation

| Violation | Consequence |
|-----------|-------------|
| Security rules (1-3) | Code rejected, security review required |
| Quality rules (4-7) | PR blocked until fixed |
| Process rules (8-10) | Team notification, mandatory fix |

---

## ✅ Pre-Commit Checklist

- [ ] No secrets in code (grep for API keys, passwords)
- [ ] All queries parameterized
- [ ] User input sanitized
- [ ] All try/except blocks have logging
- [ ] Tests written and passing
- [ ] Functions documented
- [ ] No duplicate code
- [ ] All changes committed
- [ ] No direct DOM manipulation
- [ ] All endpoints validated

---

## 🔍 Automated Checks

```yaml
# .github/workflows/security.yml
- name: Check for secrets
  run: trufflehog filesystem .

- name: Check for SQL injection
  run: bandit -r src/

- name: Check coverage
  run: pytest --cov-fail-under=80
```

---

**Violation of these rules is grounds for immediate code rejection.**
