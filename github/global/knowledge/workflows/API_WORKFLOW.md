# 🌐 API Development Workflow (Logical Workchart)

This document visualizes request routing and middleware processing.

## 1. Request Processing Pipeline

```mermaid
graph LR
    Req[Request] --> MW1[Auth Middleware]
    MW1 -->|Pass| MW2[Rate Limiter]
    MW2 -->|Pass| Router[URL Router]
    Router -->|Match| Handler[Controller Function]
    Handler -->|Call| Service[Service Layer]
    Service -->|Return| Handler
    Handler -->|Response| Res[JSON Response]
```

## 2. Example: RESTful Resource Flow

```mermaid
sequenceDiagram
    participant Client
    participant Router
    participant Controller
    participant Service

    Client->>Router: GET /items/123
    Router->>Controller: get_item(123)
    Controller->>Service: fetch_item(123)
    Service-->>Controller: Item Object
    Controller-->>Router: ItemResponse(JSON)
    Router-->>Client: 200 OK
```

### 📥 Imports (Routing)
*   **Methods**: GET, POST, PUT, DELETE.
*   **Dependencies**: Auth User, DB Session.

### 📤 Exports (Endpoints)
*   **Routes**: `/items`, `/users`.
*   **Docs**: OpenAPI / Swagger JSON.
