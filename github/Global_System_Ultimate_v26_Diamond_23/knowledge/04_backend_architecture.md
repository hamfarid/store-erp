# Backend Architecture (Global System Ultimate)

## Core Philosophy
The backend architecture follows the **Clean Architecture** principles, ensuring separation of concerns, testability, and independence from frameworks and databases.

## 7 Core Layers

### 1. API Layer (Controllers/Resolvers)
*   **Responsibility:** Handle HTTP requests, validate input (DTOs), and return responses.
*   **Rule:** Thin controllers. No business logic here. Delegate to Services.

### 2. Service Layer (Business Logic)
*   **Responsibility:** Implement core business rules, workflows, and calculations.
*   **Rule:** Framework-agnostic. Should not know about HTTP or Database details directly.

### 3. Repository Layer (Data Access)
*   **Responsibility:** Abstract database operations (CRUD).
*   **Rule:** Returns Domain Entities, not database rows. Handles ORM/SQL logic.

### 4. Domain Layer (Entities/Models)
*   **Responsibility:** Define the core data structures and rules of the business.
*   **Rule:** Pure classes/structs. No dependencies on external libraries.

### 5. Infrastructure Layer
*   **Responsibility:** Implement interfaces defined in the Domain/Service layers.
*   **Examples:** Database connections, Email services, File storage, 3rd party APIs.

### 6. Middleware & Security
*   **Authentication:** Verify identity (JWT, OAuth).
*   **Authorization:** Verify permissions (RBAC, ABAC).
*   **Logging & Monitoring:** Request tracing, error logging.

### 7. Database & Migrations
*   **Schema Management:** Version-controlled migrations (e.g., Alembic, Prisma Migrate).
*   **Optimization:** Indexing, query optimization, connection pooling.

## Best Practices

*   **Dependency Injection:** Invert control to make testing easier.
*   **SOLID Principles:** Adhere to SRP, OCP, LSP, ISP, DIP.
*   **Error Handling:** Centralized exception handling with standardized error responses.
*   **Statelessness:** Servers should be stateless to allow horizontal scaling.
*   **API Versioning:** Always version APIs (e.g., `/api/v1/resource`).
