# services_modules.board_management.models.board_member

## Imports
- board
- django.contrib.auth
- django.db
- django.utils
- django.utils.translation

## Classes
- BoardMember
  - attr: `board`
  - attr: `user`
  - attr: `name`
  - attr: `role`
  - attr: `status`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `is_active`
- Role
  - attr: `CHAIRMAN`
  - attr: `MEMBER`
  - attr: `SECRETARY`
  - attr: `OBSERVER`
- Status
  - attr: `ACTIVE`
  - attr: `INACTIVE`
  - attr: `RESIGNED`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- is_active

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class BoardMember {
        +board
        +user
        +name
        +role
        +status
        +... (4 more)
        +__str__()
        +is_active()
    }
    class Role {
        +CHAIRMAN
        +MEMBER
        +SECRETARY
        +OBSERVER
    }
    class Status {
        +ACTIVE
        +INACTIVE
        +RESIGNED
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    BoardMember --> Meta
    Role --> Meta
    Status --> Meta
```
