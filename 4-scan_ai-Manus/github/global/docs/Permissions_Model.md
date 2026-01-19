# Permissions Model

## Overview
This document describes the Role-Based Access Control (RBAC) system for the project.

## Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| Admin | Full system access | All |
| User | Standard user | Read, Create own |
| Guest | Limited access | Read only |

## Permissions Matrix

| Resource | Admin | User | Guest |
|----------|-------|------|-------|
| Users | CRUD | R | - |
| Posts | CRUD | CRUD (own) | R |
| Settings | CRUD | R | - |

## Implementation
- Use middleware to check permissions
- Store roles in database
- Cache permissions for performance
