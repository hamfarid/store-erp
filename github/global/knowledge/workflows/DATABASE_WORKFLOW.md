# 🗄️ Database Development Workflow (Logical Workchart)

This document visualizes data modeling and migration flows.

## 1. Migration Lifecycle

```mermaid
graph TD
    A[Developer] -->|Edit Model| B[models.py]
    B -->|Run Command| C[Alembic Revision]
    C -->|Generate| D[Migration Script]
    D -->|Review| E{Is Correct?}
    E -- No --> B
    E -- Yes --> F[Alembic Upgrade]
    F -->|Apply SQL| G[(PostgreSQL)]
    G -->|Update| H[Schema Version Table]
```

## 2. Entity Relationship Diagram (ERD) Example

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string email
        string password_hash
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        datetime created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id
        int quantity
    }
```

### 📥 Imports (Definitions)
*   **Types**: Integer, String, DateTime.
*   **Constraints**: Unique, ForeignKey.

### 📤 Exports (Schema)
*   **Tables**: Users, Orders.
*   **Relations**: One-to-Many.
