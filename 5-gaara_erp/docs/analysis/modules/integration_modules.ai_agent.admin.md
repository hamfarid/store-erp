# integration_modules.ai_agent.admin

## Imports
- django.contrib
- models

## Classes
- AgentTypeAdmin
  - attr: `list_display`
  - attr: `search_fields`
- AgentAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `fieldsets`
- AgentInteractionAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- AgentActivityLogAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `list_select_related`

## Class Diagram

```mermaid
classDiagram
    class AgentTypeAdmin {
        +list_display
        +search_fields
    }
    class AgentAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +fieldsets
    }
    class AgentInteractionAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class AgentActivityLogAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +list_select_related
    }
```
