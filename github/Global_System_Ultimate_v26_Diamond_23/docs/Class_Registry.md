# Class Registry

## Purpose
A quick lookup for what each class and function does.

## Backend Classes

### User
**File:** `src/backend/models/User.js`  
**Purpose:** User model with authentication  
**Methods:**
- `create()` - Create new user
- `findById()` - Find user by ID
- `authenticate()` - Verify credentials

### Database
**File:** `src/backend/db/Database.js`  
**Purpose:** Database connection manager  
**Methods:**
- `connect()` - Establish connection
- `disconnect()` - Close connection
- `query()` - Execute query

## Frontend Components

### App
**File:** `src/frontend/App.jsx`  
**Purpose:** Root component  
**Props:** None

### Header
**File:** `src/frontend/components/Header.jsx`  
**Purpose:** Navigation header  
**Props:** `user`, `onLogout`

---

(Add more classes and functions as the project grows)
