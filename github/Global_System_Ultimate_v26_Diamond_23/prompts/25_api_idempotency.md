# PROMPT: Idempotent API Design

**Objective:** Implement an idempotent API endpoint for a mutation (create, update, delete).

**Context:** You are implementing a `POST /api/items` endpoint. This endpoint must be idempotent to prevent duplicate item creation from network retries.

---

## Phase 1: Middleware

1.  **Create Middleware:** Create a file `src/backend/middleware/idempotency.js`.
2.  **Implement Logic:**
    -   Check for `Idempotency-Key` in the header.
    -   If the key exists in your cache (e.g., Redis), return the cached response.
    -   If not, call `next()` to proceed to the controller.
    -   After the controller responds, cache the response with the key.

```javascript
// src/backend/middleware/idempotency.js
const cache = require("../cache"); // Your Redis cache client

async function idempotency(req, res, next) {
  const idempotencyKey = req.headers["idempotency-key"];

  if (!idempotencyKey) {
    return next();
  }

  try {
    const cachedResponse = await cache.get(idempotencyKey);
    if (cachedResponse) {
      const parsedResponse = JSON.parse(cachedResponse);
      return res.status(parsedResponse.status).json(parsedResponse.body);
    }

    // Monkey-patch res.json to cache the response
    const originalJson = res.json;
    res.json = function (body) {
      const responseToCache = {
        status: res.statusCode,
        body: body,
      };
      cache.set(idempotencyKey, JSON.stringify(responseToCache), "EX", 24 * 60 * 60); // 24-hour TTL
      originalJson.call(this, body);
    };

    next();
  } catch (error) {
    console.error("Idempotency middleware error:", error);
    next(error);
  }
}

module.exports = idempotency;
```

## Phase 2: Route

1.  **Apply Middleware:** Apply the `idempotency` middleware to your `POST` route.

```javascript
// src/backend/routes/items.js
const express = require("express");
const router = express.Router();
const idempotency = require("../middleware/idempotency");
const itemsController = require("../controllers/itemsController");

router.post("/", idempotency, itemsController.createItem);

module.exports = router;
```

## Phase 3: Controller

1.  **Implement Controller:** Your controller logic remains the same. The middleware handles the idempotency.

```javascript
// src/backend/controllers/itemsController.js
const Item = require("../models/Item");

async function createItem(req, res) {
  try {
    const newItem = await Item.create(req.body);
    res.status(201).json(newItem);
  } catch (error) {
    res.status(500).json({ message: "Error creating item" });
  }
}

module.exports = { createItem };
```

## Phase 4: Frontend

1.  **Create Utility:** Create a utility function to handle sending the `Idempotency-Key`.

```javascript
// src/frontend/utils/api.js
import { v4 as uuidv4 } from "uuid";

export async function postItem(itemData) {
  const idempotencyKey = uuidv4();
  const response = await fetch("/api/items", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Idempotency-Key": idempotencyKey,
    },
    body: JSON.stringify(itemData),
  });

  if (!response.ok) {
    throw new Error("Failed to create item");
  }

  return response.json();
}
```

## Phase 5: Verification

1.  **Test:**
    -   Send a `POST` request with an `Idempotency-Key`.
    -   Verify the item is created and you receive a `201`.
    -   Send the **exact same request** again.
    -   Verify you receive a `201` again, but a **second item is not created** in the database.

---

**Success Criteria:**
- ✅ Middleware is created and applied.
- ✅ Controller logic is correct.
- ✅ Frontend utility is created.
- ✅ Duplicate requests do not create duplicate resources.

