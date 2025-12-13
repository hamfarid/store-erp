# REST API Best Practices

## 1. Use Proper HTTP Methods

- GET: Retrieve resources
- POST: Create resources
- PUT: Update entire resource
- PATCH: Update partial resource
- DELETE: Delete resource

## 2. Use Meaningful Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## 3. Implement Pagination

\`\`\`javascript
GET /api/users?page=1&limit=20
\`\`\`

## 4. Use Filtering and Sorting

\`\`\`javascript
GET /api/users?role=admin&sort=created_at:desc
\`\`\`

## 5. Version Your API

\`\`\`javascript
GET /api/v1/users
\`\`\`
