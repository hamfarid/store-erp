# admin_modules.notifications.models.backup_files.notification

## Imports
- django.conf
- django.db
- django.utils.translation

## Classes
- Notification
  - attr: `LEVEL_CHOICES`
  - attr: `IMPORTANCE_CHOICES`
  - attr: `recipient`
  - attr: `sender`
  - attr: `level`
  - attr: `importance`
  - attr: `title`
  - attr: `message`
  - attr: `read`
  - attr: `created_at`
  - attr: `related_task_id`
  - attr: `is_converted_to_task`
  - attr: `link`
  - attr: `module`
  - attr: `data`
  - method: `__str__`
  - method: `mark_as_read`
  - method: `mark_as_unread`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- mark_as_read
- mark_as_unread

## Class Diagram

```mermaid
classDiagram
    class Notification {
        +LEVEL_CHOICES
        +IMPORTANCE_CHOICES
        +recipient
        +sender
        +level
        +... (10 more)
        +__str__()
        +mark_as_read()
        +mark_as_unread()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    Notification --> Meta
```
