# integration_modules.ai.admin

## Imports
- django.contrib
- django.utils.translation
- models

## Classes
- LearningSourceAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- ReferenceFileAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- KeywordAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- KeywordFileAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- ConversationAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- MessageAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`

## Class Diagram

```mermaid
classDiagram
    class LearningSourceAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class ReferenceFileAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class KeywordAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class KeywordFileAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class ConversationAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class MessageAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
```
