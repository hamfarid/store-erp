# core_modules.user_permissions.models

## Imports
- core.models
- django.contrib.auth
- django.contrib.contenttypes.fields
- django.contrib.contenttypes.models
- django.db
- django.utils.translation
- permissions.models

## Classes
- UserPermission
  - attr: `SCOPE_GLOBAL`
  - attr: `SCOPE_COMPANY`
  - attr: `SCOPE_BRANCH`
  - attr: `SCOPE_DEPARTMENT`
  - attr: `SCOPE_CHOICES`
  - attr: `user`
  - attr: `permission`
  - attr: `scope`
  - attr: `content_type`
  - attr: `object_id`
  - attr: `content_object`
  - method: `__str__`
- UserRole
  - attr: `name`
  - attr: `description`
  - attr: `permissions`
  - attr: `is_active`
  - method: `__str__`
- UserRoleAssignment
  - attr: `SCOPE_GLOBAL`
  - attr: `SCOPE_COMPANY`
  - attr: `SCOPE_BRANCH`
  - attr: `SCOPE_DEPARTMENT`
  - attr: `SCOPE_CHOICES`
  - attr: `user`
  - attr: `role`
  - attr: `scope`
  - attr: `content_type`
  - attr: `object_id`
  - attr: `content_object`
  - method: `__str__`
- PermissionRequest
  - attr: `STATUS_PENDING`
  - attr: `STATUS_APPROVED`
  - attr: `STATUS_REJECTED`
  - attr: `STATUS_CHOICES`
  - attr: `user`
  - attr: `permission`
  - attr: `reason`
  - attr: `status`
  - attr: `reviewed_by`
  - attr: `reviewed_at`
  - attr: `review_notes`
  - attr: `content_type`
  - attr: `object_id`
  - attr: `content_object`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- check_user_permission
- get_user_permissions
- get_users_with_permission
- __str__
- __str__
- __str__
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserPermission {
        +SCOPE_GLOBAL
        +SCOPE_COMPANY
        +SCOPE_BRANCH
        +SCOPE_DEPARTMENT
        +SCOPE_CHOICES
        +... (6 more)
        +__str__()
    }
    class UserRole {
        +name
        +description
        +permissions
        +is_active
        +__str__()
    }
    class UserRoleAssignment {
        +SCOPE_GLOBAL
        +SCOPE_COMPANY
        +SCOPE_BRANCH
        +SCOPE_DEPARTMENT
        +SCOPE_CHOICES
        +... (6 more)
        +__str__()
    }
    class PermissionRequest {
        +STATUS_PENDING
        +STATUS_APPROVED
        +STATUS_REJECTED
        +STATUS_CHOICES
        +user
        +... (9 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
        +indexes
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    UserPermission --> Meta
    UserPermission --> Meta
    UserPermission --> Meta
    UserPermission --> Meta
    UserRole --> Meta
    UserRole --> Meta
    UserRole --> Meta
    UserRole --> Meta
    UserRoleAssignment --> Meta
    UserRoleAssignment --> Meta
    UserRoleAssignment --> Meta
    UserRoleAssignment --> Meta
    PermissionRequest --> Meta
    PermissionRequest --> Meta
    PermissionRequest --> Meta
    PermissionRequest --> Meta
```
