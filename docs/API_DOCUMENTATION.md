> This is a template. Fill this out for your specific project.

# API Documentation

**Version:** 1.0  
**Base URL:** `/api/v1`

---

## 1. Authentication

*Describe how to authenticate with the API. Is it API keys, OAuth 2.0, JWT? Provide examples.*

**Example: Bearer Token**

All API requests must include an `Authorization` header with a valid JWT token.

```http
Authorization: Bearer <YOUR_JWT_TOKEN>
```

## 2. Rate Limiting

- **Standard Limit:** 100 requests per minute per IP address.
- **Authenticated Limit:** 1000 requests per minute per user.

## 3. Error Handling

*Describe the common error codes and their meanings.*

| Status Code | Meaning               | Description                                      |
|-------------|-----------------------|--------------------------------------------------|
| `400`       | Bad Request           | The request was malformed or invalid.            |
| `401`       | Unauthorized          | Authentication failed or is required.            |
| `403`       | Forbidden             | You do not have permission to access this resource.|
| `404`       | Not Found             | The requested resource could not be found.       |
| `429`       | Too Many Requests     | You have exceeded the rate limit.                |
| `500`       | Internal Server Error | Something went wrong on our end.                 |

**Error Response Body:**

```json
{
  "error": {
    "message": "A human-readable error message."
  }
}
```

---

## 4. Endpoints

*Document each API endpoint in detail.*

### Users

#### `GET /users`

- **Description:** Retrieve a list of all users.
- **Permissions:** `admin`
- **Query Parameters:**
    - `page` (integer, optional, default: 1): The page number for pagination.
    - `limit` (integer, optional, default: 20): The number of results per page.
- **Success Response (200 OK):**

```json
{
  "data": [
    {
      "id": "user-123",
      "name": "Alice",
      "email": "alice@example.com"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

#### `POST /users`

- **Description:** Create a new user.
- **Permissions:** `admin`
- **Request Body:**

```json
{
  "name": "Bob",
  "email": "bob@example.com",
  "password": "strongpassword123"
}
```

- **Success Response (201 Created):**

```json
{
  "data": {
    "id": "user-456",
    "name": "Bob",
    "email": "bob@example.com"
  }
}
```

#### `GET /users/{id}`

- **Description:** Retrieve a single user by their ID.
- **Permissions:** `admin` or owner of the user account.
- **Path Parameters:**
    - `id` (string, required): The ID of the user to retrieve.
- **Success Response (200 OK):**

```json
{
  "data": {
    "id": "user-123",
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

- **Error Response (404 Not Found):**

```json
{
  "error": {
    "message": "User not found."
  }
}
```

