# core_modules.users_accounts.serializers

## Imports
- admin_modules.permissions_manager.models
- admin_modules.permissions_manager.serializers
- django.contrib.auth
- rest_framework

## Classes
- UserRoleAssignmentSerializer
  - attr: `role_name`
  - attr: `role_id`
- UserSerializer
  - method: `create`
  - method: `update`
- BasicRoleSerializer
- BasicPermissionSerializer
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
  - attr: `extra_kwargs`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Functions
- create
- update

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserRoleAssignmentSerializer {
        +role_name
        +role_id
    }
    class UserSerializer {
        +create()
        +update()
    }
    class BasicRoleSerializer {
    }
    class BasicPermissionSerializer {
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
        +extra_kwargs
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    UserRoleAssignmentSerializer --> Meta
    UserRoleAssignmentSerializer --> Meta
    UserRoleAssignmentSerializer --> Meta
    UserRoleAssignmentSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    BasicRoleSerializer --> Meta
    BasicRoleSerializer --> Meta
    BasicRoleSerializer --> Meta
    BasicRoleSerializer --> Meta
    BasicPermissionSerializer --> Meta
    BasicPermissionSerializer --> Meta
    BasicPermissionSerializer --> Meta
    BasicPermissionSerializer --> Meta
```
