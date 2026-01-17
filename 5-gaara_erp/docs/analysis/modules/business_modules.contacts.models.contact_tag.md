# business_modules.contacts.models.contact_tag

## Imports
- django.db
- django.utils.translation

## Classes
- ContactTag
  - attr: `name`
  - attr: `color`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class ContactTag {
        +name
        +color
        +is_active
        +created_at
        +updated_at
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    ContactTag --> Meta
```
