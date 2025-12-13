# دليل تفعيل Global Guidelines في مشروع Store

**الإصدار:** 7.1.1  
**التاريخ:** 2025-11-03  
**المشروع:** Store (E-commerce Platform)

---

## 📖 نظرة عامة

هذا الدليل يوضح كيفية تفعيل واستخدام Global Guidelines v7.1.1 في مشروع Store القائم، مع الاستفادة من جميع الميزات المتقدمة بما في ذلك إدارة الذاكرة والتكامل مع MCP.

---

## 🎯 الأهداف

1. ✅ تفعيل البرومبت في مشروع Store
2. ✅ إعداد نظام الذاكرة للمشروع
3. ✅ تكوين MCP servers المناسبة
4. ✅ إنشاء خرائط المشروع الإلزامية
5. ✅ بدء استخدام الميزات المتقدمة

---

## 📋 المتطلبات الأساسية

### 1. البرمجيات المطلوبة

```bash
# Python 3.8+
python3 --version

# Node.js 16+ (للمشروع)
node --version

# Git
git --version

# PostgreSQL (للذاكرة - اختياري)
psql --version

# Redis (للذاكرة - اختياري)
redis-cli --version
```

### 2. المشروع القائم

```bash
# تأكد من وجود مشروع Store
ls -la ~/Store/

# البنية المتوقعة:
# Store/
# ├── backend/
# ├── frontend/
# ├── database/
# └── README.md
```

---

## 🚀 خطوات التفعيل

### المرحلة 1: إعداد البيئة (10 دقائق)

#### 1.1 استنساخ Global Guidelines

```bash
# في مجلد المشاريع
cd ~/

# استنساخ المستودع
git clone https://github.com/hamfarid/global.git

# الانتقال إلى المجلد
cd global

# التحقق من الإصدار
cat README.md | head -5
```

#### 1.2 إنشاء مجلد الذاكرة في Store

```bash
# الانتقال إلى مشروع Store
cd ~/Store

# إنشاء مجلد الذاكرة
mkdir -p .memory/{conversations,knowledge,preferences,state,checkpoints,vectors}

# نسخ ملفات الإعداد
cp ~/global/.memory/README.md .memory/
cp ~/global/.memory/setup_example.py .memory/

# تشغيل الإعداد
cd .memory
python3 setup_example.py
```

#### 1.3 تحديث .gitignore

```bash
# في مجلد Store
cd ~/Store

# إضافة قواعد الذاكرة إلى .gitignore
cat >> .gitignore << 'EOF'

# AI Memory System (local only)
.memory/conversations/*.json
.memory/knowledge/*.json
.memory/preferences/*.json
.memory/state/*.json
.memory/checkpoints/*.json
.memory/vectors/*
!.memory/vectors/.gitkeep
*.db
*.sqlite
*.sqlite3
redis-data/
chroma_data/
memory_backups/

EOF

echo "✅ .gitignore updated"
```

---

### المرحلة 2: إنشاء خرائط المشروع الإلزامية (30 دقائق)

وفقاً لـ Module 16، يجب إنشاء 7 خرائط قبل البدء:

#### 2.1 Project Structure Map

```bash
cd ~/Store

# إنشاء مجلد للخرائط
mkdir -p .ai_maps

# إنشاء خريطة البنية
cat > .ai_maps/01_project_structure.mmd << 'EOF'
graph TD
    Store[Store Project]
    
    Store --> Backend[Backend - Node.js/Express]
    Store --> Frontend[Frontend - React]
    Store --> Database[Database - PostgreSQL]
    Store --> Shared[Shared - Types/Utils]
    
    Backend --> API[API Routes]
    Backend --> Controllers[Controllers]
    Backend --> Models[Models]
    Backend --> Middleware[Middleware]
    Backend --> Services[Services]
    
    Frontend --> Components[Components]
    Frontend --> Pages[Pages]
    Frontend --> Hooks[Hooks]
    Frontend --> Context[Context]
    Frontend --> Utils[Utils]
    
    Database --> Schema[Schema]
    Database --> Migrations[Migrations]
    Database --> Seeds[Seeds]
    
    API --> Products[/api/products]
    API --> Orders[/api/orders]
    API --> Users[/api/users]
    API --> Auth[/api/auth]
    API --> Cart[/api/cart]
    API --> Payment[/api/payment]
EOF

echo "✅ Project structure map created"
```

#### 2.2 Imports & Exports Map

```bash
cd ~/Store

# إنشاء خريطة الاستيرادات والتصديرات
cat > .ai_maps/02_imports_exports.json << 'EOF'
{
  "backend": {
    "exports": {
      "api": [
        "/api/products - GET, POST, PUT, DELETE",
        "/api/orders - GET, POST, PUT",
        "/api/users - GET, POST, PUT, DELETE",
        "/api/auth - POST /login, POST /register, POST /logout",
        "/api/cart - GET, POST, PUT, DELETE",
        "/api/payment - POST /process"
      ],
      "models": [
        "Product",
        "Order",
        "User",
        "Cart",
        "Payment"
      ]
    },
    "imports": {
      "express": "^4.18.0",
      "pg": "^8.11.0",
      "bcrypt": "^5.1.0",
      "jsonwebtoken": "^9.0.0",
      "cors": "^2.8.5",
      "dotenv": "^16.0.0"
    }
  },
  "frontend": {
    "exports": {
      "components": [
        "ProductCard",
        "ProductList",
        "Cart",
        "Checkout",
        "UserProfile",
        "Navigation"
      ],
      "pages": [
        "Home",
        "Products",
        "ProductDetail",
        "Cart",
        "Checkout",
        "Profile",
        "Login",
        "Register"
      ]
    },
    "imports": {
      "react": "^18.2.0",
      "react-router-dom": "^6.10.0",
      "axios": "^1.4.0",
      "react-query": "^3.39.0",
      "@mui/material": "^5.13.0"
    }
  },
  "shared": {
    "types": [
      "Product",
      "Order",
      "User",
      "Cart",
      "CartItem",
      "Payment"
    ]
  }
}
EOF

echo "✅ Imports/Exports map created"
```

#### 2.3 Class Definitions Map

```bash
cd ~/Store

# إنشاء خريطة الفئات
cat > .ai_maps/03_class_definitions.puml << 'EOF'
@startuml Store Classes

' Models
class Product {
  +id: number
  +name: string
  +description: string
  +price: number
  +stock: number
  +category: string
  +images: string[]
  +createdAt: Date
  +updatedAt: Date
  --
  +validate(): boolean
  +toJSON(): object
}

class User {
  +id: number
  +email: string
  +password: string (hashed)
  +name: string
  +phone: string
  +address: Address
  +role: UserRole
  +createdAt: Date
  --
  +authenticate(password): boolean
  +generateToken(): string
  +toJSON(): object
}

class Order {
  +id: number
  +userId: number
  +items: OrderItem[]
  +total: number
  +status: OrderStatus
  +shippingAddress: Address
  +paymentMethod: string
  +createdAt: Date
  --
  +calculateTotal(): number
  +updateStatus(status): void
  +toJSON(): object
}

class Cart {
  +id: number
  +userId: number
  +items: CartItem[]
  +createdAt: Date
  +updatedAt: Date
  --
  +addItem(product, quantity): void
  +removeItem(productId): void
  +updateQuantity(productId, quantity): void
  +calculateTotal(): number
  +clear(): void
}

class Payment {
  +id: number
  +orderId: number
  +amount: number
  +method: string
  +status: PaymentStatus
  +transactionId: string
  +createdAt: Date
  --
  +process(): Promise<boolean>
  +refund(): Promise<boolean>
  +verify(): boolean
}

' Relationships
User "1" -- "0..*" Order : places
User "1" -- "1" Cart : has
Order "1" -- "1" Payment : requires
Order "1" *-- "*" OrderItem : contains
Cart "1" *-- "*" CartItem : contains
Product "1" -- "*" OrderItem : in
Product "1" -- "*" CartItem : in

' Enums
enum UserRole {
  CUSTOMER
  ADMIN
  SELLER
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

enum PaymentStatus {
  PENDING
  COMPLETED
  FAILED
  REFUNDED
}

@enduml
EOF

echo "✅ Class definitions map created"
```

#### 2.4 Libraries & Dependencies Map

```bash
cd ~/Store

# إنشاء خريطة المكتبات
cat > .ai_maps/04_libraries_dependencies.json << 'EOF'
{
  "backend": {
    "runtime": "Node.js 18.x",
    "framework": "Express 4.18.x",
    "dependencies": {
      "core": {
        "express": "^4.18.0",
        "pg": "^8.11.0",
        "dotenv": "^16.0.0"
      },
      "authentication": {
        "bcrypt": "^5.1.0",
        "jsonwebtoken": "^9.0.0",
        "passport": "^0.6.0"
      },
      "validation": {
        "joi": "^17.9.0",
        "express-validator": "^7.0.0"
      },
      "utilities": {
        "cors": "^2.8.5",
        "morgan": "^1.10.0",
        "helmet": "^7.0.0",
        "compression": "^1.7.4"
      }
    },
    "devDependencies": {
      "testing": {
        "jest": "^29.5.0",
        "supertest": "^6.3.0"
      },
      "development": {
        "nodemon": "^2.0.22",
        "eslint": "^8.42.0",
        "prettier": "^2.8.8"
      }
    }
  },
  "frontend": {
    "runtime": "React 18.x",
    "bundler": "Vite 4.x",
    "dependencies": {
      "core": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.10.0"
      },
      "state_management": {
        "react-query": "^3.39.0",
        "zustand": "^4.3.0"
      },
      "ui": {
        "@mui/material": "^5.13.0",
        "@mui/icons-material": "^5.13.0",
        "@emotion/react": "^11.11.0",
        "@emotion/styled": "^11.11.0"
      },
      "http": {
        "axios": "^1.4.0"
      },
      "forms": {
        "react-hook-form": "^7.44.0",
        "yup": "^1.2.0"
      }
    },
    "devDependencies": {
      "vite": "^4.3.0",
      "eslint": "^8.42.0",
      "prettier": "^2.8.8"
    }
  },
  "database": {
    "system": "PostgreSQL 15.x",
    "orm": "None (raw SQL)",
    "migrations": "node-pg-migrate"
  }
}
EOF

echo "✅ Libraries/Dependencies map created"
```

#### 2.5 API Endpoints Map

```bash
cd ~/Store

# إنشاء خريطة API
cat > .ai_maps/05_api_endpoints.yaml << 'EOF'
openapi: 3.0.0
info:
  title: Store API
  version: 1.0.0
  description: E-commerce Store API

servers:
  - url: http://localhost:5000/api
    description: Development server

paths:
  /products:
    get:
      summary: Get all products
      parameters:
        - name: category
          in: query
          schema:
            type: string
        - name: page
          in: query
          schema:
            type: integer
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: List of products
    post:
      summary: Create new product
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Product'
      responses:
        '201':
          description: Product created

  /products/{id}:
    get:
      summary: Get product by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Product details
    put:
      summary: Update product
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Product'
      responses:
        '200':
          description: Product updated
    delete:
      summary: Delete product
      security:
        - bearerAuth: []
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Product deleted

  /auth/register:
    post:
      summary: Register new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
                name:
                  type: string
      responses:
        '201':
          description: User registered

  /auth/login:
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'

  /cart:
    get:
      summary: Get user cart
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Cart details
    post:
      summary: Add item to cart
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                productId:
                  type: integer
                quantity:
                  type: integer
      responses:
        '200':
          description: Item added

  /orders:
    get:
      summary: Get user orders
      security:
        - bearerAuth: []
      responses:
        '200':
          description: List of orders
    post:
      summary: Create new order
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      responses:
        '201':
          description: Order created

  /payment/process:
    post:
      summary: Process payment
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                orderId:
                  type: integer
                paymentMethod:
                  type: string
                cardDetails:
                  type: object
      responses:
        '200':
          description: Payment processed

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Product:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        price:
          type: number
        stock:
          type: integer
        category:
          type: string
        images:
          type: array
          items:
            type: string

    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
        name:
          type: string
        phone:
          type: string
        role:
          type: string

    Order:
      type: object
      properties:
        id:
          type: integer
        userId:
          type: integer
        items:
          type: array
          items:
            type: object
        total:
          type: number
        status:
          type: string
        shippingAddress:
          type: object
EOF

echo "✅ API endpoints map created"
```

#### 2.6 Database Schema Map

```bash
cd ~/Store

# إنشاء خريطة قاعدة البيانات
cat > .ai_maps/06_database_schema.sql << 'EOF'
-- Store Database Schema

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(20) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    category VARCHAR(100),
    images JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    shipping_address JSONB,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart table
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart items table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id)
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE REFERENCES orders(id),
    amount DECIMAL(10, 2) NOT NULL,
    method VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_payments_order_id ON payments(order_id);

-- ERD Diagram (Mermaid)
-- erDiagram
--     USERS ||--o{ ORDERS : places
--     USERS ||--|| CARTS : has
--     ORDERS ||--|| PAYMENTS : requires
--     ORDERS ||--o{ ORDER_ITEMS : contains
--     CARTS ||--o{ CART_ITEMS : contains
--     PRODUCTS ||--o{ ORDER_ITEMS : in
--     PRODUCTS ||--o{ CART_ITEMS : in
EOF

echo "✅ Database schema map created"
```

#### 2.7 Configuration Map

```bash
cd ~/Store

# إنشاء خريطة الإعدادات
cat > .ai_maps/07_configuration.json << 'EOF'
{
  "environment": {
    "development": {
      "backend": {
        "PORT": 5000,
        "NODE_ENV": "development",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/store_dev",
        "JWT_SECRET": "dev-secret-key",
        "JWT_EXPIRES_IN": "7d",
        "CORS_ORIGIN": "http://localhost:3000"
      },
      "frontend": {
        "PORT": 3000,
        "VITE_API_URL": "http://localhost:5000/api"
      },
      "database": {
        "host": "localhost",
        "port": 5432,
        "database": "store_dev",
        "user": "postgres",
        "password": "postgres"
      }
    },
    "production": {
      "backend": {
        "PORT": "${PORT}",
        "NODE_ENV": "production",
        "DATABASE_URL": "${DATABASE_URL}",
        "JWT_SECRET": "${JWT_SECRET}",
        "JWT_EXPIRES_IN": "7d",
        "CORS_ORIGIN": "${FRONTEND_URL}"
      },
      "frontend": {
        "VITE_API_URL": "${API_URL}"
      }
    }
  },
  "features": {
    "authentication": true,
    "cart": true,
    "checkout": true,
    "payment": true,
    "admin_panel": false,
    "reviews": false,
    "wishlist": false
  },
  "integrations": {
    "payment_gateway": "stripe",
    "email_service": "sendgrid",
    "storage": "local",
    "analytics": "google-analytics"
  }
}
EOF

echo "✅ Configuration map created"
```

#### 2.8 إنشاء ملف فهرس للخرائط

```bash
cd ~/Store

# إنشاء فهرس الخرائط
cat > .ai_maps/README.md << 'EOF'
# AI Project Maps - Store

This directory contains the 7 mandatory project maps required by Global Guidelines Module 16.

## Maps

1. **01_project_structure.mmd** - Mermaid diagram of project structure
2. **02_imports_exports.json** - JSON mapping of imports/exports
3. **03_class_definitions.puml** - PlantUML class diagram
4. **04_libraries_dependencies.json** - JSON of all dependencies
5. **05_api_endpoints.yaml** - OpenAPI specification
6. **06_database_schema.sql** - SQL schema + ERD
7. **07_configuration.json** - Environment configuration

## Usage

These maps are used by AI to:
- Understand project structure
- Navigate codebase efficiently
- Make informed decisions
- Avoid breaking changes
- Suggest improvements

## Updating

Update maps when:
- Adding new features
- Changing architecture
- Adding dependencies
- Modifying API
- Changing database schema

## Tools

Generate diagrams:
```bash
# Mermaid
npx @mermaid-js/mermaid-cli -i 01_project_structure.mmd -o structure.png

# PlantUML
plantuml 03_class_definitions.puml
```
EOF

echo "✅ Maps index created"
echo ""
echo "📊 جميع الخرائط الإلزامية تم إنشاؤها في .ai_maps/"
```

---

### المرحلة 3: إعداد نظام الذاكرة (15 دقائق)

#### 3.1 تهيئة نظام الذاكرة

```python
# في ~/Store/.memory/init_memory.py

from pathlib import Path
import json
from datetime import datetime

def init_store_memory():
    """Initialize memory system for Store project."""
    
    # Store project preferences
    preferences = {
        "user_id": "store_dev",
        "project": "Store",
        "preferences": {
            "backend": {
                "language": "javascript",
                "framework": "express",
                "database": "postgresql",
                "orm": "none"
            },
            "frontend": {
                "framework": "react",
                "ui_library": "mui",
                "state_management": "react-query + zustand",
                "styling": "emotion"
            },
            "testing": {
                "backend": "jest + supertest",
                "frontend": "vitest + testing-library"
            },
            "deployment": {
                "backend": "heroku",
                "frontend": "vercel",
                "database": "heroku-postgres"
            }
        },
        "updated_at": datetime.now().isoformat()
    }
    
    # Save preferences
    prefs_file = Path("preferences/store_dev.json")
    with open(prefs_file, 'w') as f:
        json.dump(preferences, f, indent=2)
    print(f"✅ Preferences saved: {prefs_file}")
    
    # Store initial state
    state = {
        "user_id": "store_dev",
        "current_project": "Store",
        "current_phase": "development",
        "context": {
            "stack": ["Node.js", "Express", "React", "PostgreSQL"],
            "phase": "implementation",
            "features_completed": [
                "User authentication",
                "Product listing",
                "Cart functionality"
            ],
            "features_in_progress": [
                "Checkout process",
                "Payment integration"
            ],
            "features_planned": [
                "Admin panel",
                "Product reviews",
                "Wishlist"
            ]
        },
        "updated_at": datetime.now().isoformat()
    }
    
    # Save state
    state_file = Path("state/current_state.json")
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ State saved: {state_file}")
    
    # Store initial knowledge
    knowledge = [
        {
            "id": "know_001",
            "type": "semantic",
            "content": "Store uses JWT for authentication with 7-day expiration",
            "importance": 9,
            "metadata": {
                "category": "authentication",
                "project": "Store"
            },
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "know_002",
            "type": "semantic",
            "content": "Database uses PostgreSQL with raw SQL queries (no ORM)",
            "importance": 8,
            "metadata": {
                "category": "database",
                "project": "Store"
            },
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "know_003",
            "type": "procedural",
            "content": "Always validate user input with Joi before processing",
            "importance": 9,
            "metadata": {
                "category": "security",
                "project": "Store"
            },
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # Save knowledge
    for item in knowledge:
        know_file = Path(f"knowledge/{item['id']}.json")
        with open(know_file, 'w') as f:
            json.dump(item, f, indent=2)
        print(f"✅ Knowledge saved: {know_file}")
    
    print("\n✅ Memory system initialized for Store project!")

if __name__ == '__main__':
    init_store_memory()
```

```bash
# تشغيل التهيئة
cd ~/Store/.memory
python3 init_memory.py
```

#### 3.2 إعداد قواعد البيانات (اختياري)

```bash
# PostgreSQL للذاكرة طويلة المدى
createdb store_ai_memory

# Redis للذاكرة قصيرة المدى (اختياري)
redis-server --daemonize yes
```

---

### المرحلة 4: تكوين MCP Servers (20 دقائق)

#### 4.1 تحديد MCP Servers المطلوبة

للمشروع Store، نحتاج:

1. **GitHub MCP** - إدارة الكود
2. **Playwright MCP** - اختبار الواجهة
3. **Sentry MCP** - تتبع الأخطاء
4. **Context7 MCP** - وثائق محدثة
5. **Sequential Thinking MCP** - حل المشاكل

#### 4.2 تكوين MCP Servers

```bash
cd ~/Store

# إنشاء ملف تكوين MCP
cat > .mcp_config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"],
      "env": {}
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": {
        "SENTRY_AUTH_TOKEN": "${SENTRY_AUTH_TOKEN}",
        "SENTRY_ORG": "your-org",
        "SENTRY_PROJECT": "store"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "context7-mcp"],
      "env": {}
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "env": {}
    }
  }
}
EOF

echo "✅ MCP configuration created"
```

#### 4.3 إنشاء ملف بيئة

```bash
cd ~/Store

# إنشاء .env.example
cat > .env.example << 'EOF'
# Backend
PORT=5000
NODE_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/store_dev
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=7d
CORS_ORIGIN=http://localhost:3000

# MCP Servers
GITHUB_TOKEN=your-github-token
SENTRY_AUTH_TOKEN=your-sentry-token

# Optional
REDIS_URL=redis://localhost:6379
CHROMA_DB_PATH=.memory/vectors
EOF

echo "✅ .env.example created"
echo "⚠️  Copy to .env and fill in your values"
```

---

### المرحلة 5: بدء الاستخدام (10 دقائق)

#### 5.1 استخدام البرومبت

```bash
# الطريقة 1: النسخة المودولية (موصى بها)
cd ~/global

# اقرأ MASTER prompt
cat prompts/00_MASTER.txt

# استخدم المودولات حسب الحاجة
cat prompts/10_backend.txt      # للعمل على Backend
cat prompts/11_frontend.txt     # للعمل على Frontend
cat prompts/60_memory_management.txt  # لإدارة الذاكرة

# الطريقة 2: النسخة الموحدة
cat GLOBAL_GUIDELINES_UNIFIED_v7.1.0.txt
```

#### 5.2 مثال عملي: إضافة ميزة جديدة

```bash
# مثال: إضافة نظام المراجعات

# 1. استخدم Thinking Framework (Module 17)
# - حدد المشكلة
# - قسم إلى مهام
# - صمم الحل

# 2. استخدم MCP Integration (Module 16)
# - أنشئ خريطة للميزة الجديدة
# - حدد التأثيرات على النظام

# 3. استخدم Backend Guidelines (Module 10)
# - صمم API endpoints
# - أنشئ Models
# - اكتب Controllers

# 4. استخدم Database Guidelines (Module 12)
# - صمم Schema
# - أنشئ Migration

# 5. استخدم Frontend Guidelines (Module 11)
# - صمم Components
# - أنشئ Pages

# 6. استخدم Testing Guidelines (Module 31)
# - اكتب Unit tests
# - اكتب Integration tests

# 7. استخدم Memory Management (Module 60)
# - احفظ القرارات
# - وثق الدروس المستفادة
```

#### 5.3 إنشاء Checkpoint

```python
# في ~/Store/.memory/create_checkpoint.py

import json
from datetime import datetime
from pathlib import Path

def create_checkpoint(name, description):
    """Create a checkpoint of current project state."""
    
    checkpoint = {
        "checkpoint_id": f"cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "name": name,
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "state": {
            "project": "Store",
            "phase": "development",
            "features_completed": [
                "User authentication",
                "Product listing",
                "Cart functionality",
                "Checkout process"
            ],
            "git_commit": "abc123...",  # Get from git
            "database_version": "001",
            "dependencies_hash": "xyz789..."  # Get from package.json
        }
    }
    
    # Save checkpoint
    cp_file = Path(f"checkpoints/{checkpoint['checkpoint_id']}_{name}.json")
    with open(cp_file, 'w') as f:
        json.dump(checkpoint, f, indent=2)
    
    print(f"✅ Checkpoint created: {cp_file}")
    return checkpoint

if __name__ == '__main__':
    create_checkpoint(
        "after_checkout_implementation",
        "Completed checkout process with payment integration"
    )
```

---

## 📚 المراجع السريعة

### الأوامر الأساسية

```bash
# عرض MASTER prompt
cat ~/global/prompts/00_MASTER.txt

# عرض مودول معين
cat ~/global/prompts/[MODULE_NUMBER]_[MODULE_NAME].txt

# عرض النسخة الموحدة
cat ~/global/GLOBAL_GUIDELINES_UNIFIED_v7.1.0.txt

# إنشاء checkpoint
cd ~/Store/.memory
python3 create_checkpoint.py

# عرض الخرائط
ls -la ~/Store/.ai_maps/
```

### المودولات المهمة لـ Store

| المودول | الاستخدام |
|---------|-----------|
| 00 | MASTER - نقطة البداية |
| 10 | Backend - Express/Node.js |
| 11 | Frontend - React |
| 12 | Database - PostgreSQL |
| 13 | API - REST APIs |
| 15 | MCP - التكامل مع الأدوات |
| 16 | MCP Integration - الخرائط والتنسيق |
| 20 | Security - الأمان |
| 21 | Authentication - JWT |
| 30 | Quality - جودة الكود |
| 31 | Testing - الاختبارات |
| 60 | Memory - إدارة الذاكرة |

---

## ✅ قائمة التحقق النهائية

### الإعداد الأساسي
- [ ] استنساخ Global Guidelines
- [ ] إنشاء مجلد .memory في Store
- [ ] تحديث .gitignore
- [ ] إنشاء الخرائط السبعة الإلزامية

### نظام الذاكرة
- [ ] تشغيل setup_example.py
- [ ] تهيئة الذاكرة للمشروع (init_memory.py)
- [ ] إعداد PostgreSQL (اختياري)
- [ ] إعداد Redis (اختياري)

### MCP Servers
- [ ] إنشاء .mcp_config.json
- [ ] إنشاء .env من .env.example
- [ ] تكوين GitHub token
- [ ] تكوين Sentry token (اختياري)

### الاستخدام
- [ ] قراءة MASTER prompt
- [ ] قراءة المودولات ذات الصلة
- [ ] إنشاء checkpoint أولي
- [ ] البدء في استخدام البرومبت

---

## 🎯 الخطوات التالية

1. **استكشف المودولات** - اقرأ المودولات المتعلقة بعملك الحالي
2. **استخدم الخرائط** - ارجع إلى الخرائط عند اتخاذ القرارات
3. **احفظ المعرفة** - وثق القرارات والدروس في نظام الذاكرة
4. **أنشئ Checkpoints** - احفظ حالة المشروع عند المعالم المهمة
5. **استفد من MCP** - استخدم الأدوات المتكاملة للأتمتة

---

## 📞 الدعم

### الموارد
- **README:** ~/global/README.md
- **Memory Guide:** ~/global/.memory/README.md
- **Module 60:** ~/global/prompts/60_memory_management.txt
- **Examples:** ~/global/PRACTICAL_EXAMPLES.md

### المساعدة
1. راجع التوثيق
2. افحص الأمثلة
3. افتح issue على GitHub

---

**تم إنشاؤه بواسطة:** Global Guidelines v7.1.1  
**التاريخ:** 2025-11-03  
**الحالة:** جاهز للاستخدام ✅

