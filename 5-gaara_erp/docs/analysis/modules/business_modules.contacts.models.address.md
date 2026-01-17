# business_modules.contacts.models.address

## Imports
- django.db
- django.utils.translation

## Classes
- Address
  - attr: `street`
  - attr: `city`
  - attr: `country`
  - attr: `postal_code`
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
    class Address {
        +street
        +city
        +country
        +postal_code
        +created_at
        +... (1 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    Address --> Meta
```
