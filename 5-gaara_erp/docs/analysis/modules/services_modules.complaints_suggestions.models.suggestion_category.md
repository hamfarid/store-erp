# services_modules.complaints_suggestions.models.suggestion_category

## Imports
- django.db
- django.db.models
- django.utils.translation
- services_modules.core.models

## Classes
- SuggestionCategory
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `get_active_suggestions_count`
  - method: `get_implemented_suggestions_count`
  - method: `get_suggestions_by_status`
  - method: `deactivate`
  - method: `activate`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`

## Functions
- __str__
- get_active_suggestions_count
- get_implemented_suggestions_count
- get_suggestions_by_status
- deactivate
- activate

## Class Diagram

```mermaid
classDiagram
    class SuggestionCategory {
        +name
        +code
        +company
        +description
        +is_active
        +... (2 more)
        +__str__()
        +get_active_suggestions_count()
        +get_implemented_suggestions_count()
        +get_suggestions_by_status()
        +deactivate()
        +... (1 more)
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
    }
    SuggestionCategory --> Meta
```
