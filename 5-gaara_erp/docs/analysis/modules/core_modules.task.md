# core_modules.task

## Imports
- django.contrib.auth
- django.db
- django.utils.translation

## Classes
- TaskBoard
  - attr: `name`
  - attr: `description`
  - attr: `owner`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- TaskList
  - attr: `name`
  - attr: `board`
  - attr: `order`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Task
  - attr: `STATUS_CHOICES`
  - attr: `PRIORITY_CHOICES`
  - attr: `title`
  - attr: `description`
  - attr: `status`
  - attr: `priority`
  - attr: `due_date`
  - attr: `created_by`
  - attr: `assigned_to`
  - attr: `task_list`
  - attr: `order`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- TaskComment
  - attr: `task`
  - attr: `user`
  - attr: `content`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- TaskAttachment
  - attr: `task`
  - attr: `file`
  - attr: `file_name`
  - attr: `uploaded_by`
  - attr: `uploaded_at`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class TaskBoard {
        +name
        +description
        +owner
        +created_at
        +updated_at
        +__str__()
    }
    class TaskList {
        +name
        +board
        +order
        +created_at
        +updated_at
        +__str__()
    }
    class Task {
        +STATUS_CHOICES
        +PRIORITY_CHOICES
        +title
        +description
        +status
        +... (8 more)
        +__str__()
    }
    class TaskComment {
        +task
        +user
        +content
        +created_at
        +updated_at
        +__str__()
    }
    class TaskAttachment {
        +task
        +file
        +file_name
        +uploaded_by
        +uploaded_at
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    TaskBoard --> Meta
    TaskBoard --> Meta
    TaskBoard --> Meta
    TaskBoard --> Meta
    TaskBoard --> Meta
    TaskList --> Meta
    TaskList --> Meta
    TaskList --> Meta
    TaskList --> Meta
    TaskList --> Meta
    Task --> Meta
    Task --> Meta
    Task --> Meta
    Task --> Meta
    Task --> Meta
    TaskComment --> Meta
    TaskComment --> Meta
    TaskComment --> Meta
    TaskComment --> Meta
    TaskComment --> Meta
    TaskAttachment --> Meta
    TaskAttachment --> Meta
    TaskAttachment --> Meta
    TaskAttachment --> Meta
    TaskAttachment --> Meta
```
