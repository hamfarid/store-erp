# REST API Best Practices (Global System Ultimate)

**Engine:** Speckit Global System Ultimate
**Status:** MANDATORY REFERENCE

## 1. Speckit Plan: API Design
Before coding, you MUST define the contract in `API_DOCUMENTATION.md`.

## 2. Core Principles
1.  **Resource-Oriented:** `/api/v1/resources` (Nouns, Plural).
2.  **Stateless:** No session state on server (Use JWT).
3.  **Versioning:** `/api/v1/` is MANDATORY.

## 3. Implementation Example (FastAPI)

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str

@app.post("/api/v1/users", status_code=201)
async def create_user(user: UserCreate):
    # Sentinel Check: Validation is handled by Pydantic
    # [Verification Oath] I have confirmed db.create exists.
    db_user = await db.create(user)
    return {"data": db_user}

@app.get("/api/v1/users")
async def list_users(
    page: int = Query(1, ge=1), 
    limit: int = Query(20, le=100)
):
    # Sentinel Check: Pagination is enforced
    users = await db.get_all(skip=(page-1)*limit, limit=limit)
    return {
        "data": users,
        "meta": {"page": page, "limit": limit}
    }
```

## 4. Speckit Verify
Run `speckit verify --api` to check:
1.  Status codes correctness.
2.  Response structure consistency.
3.  Error handling.
