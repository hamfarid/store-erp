# integration_modules.ai_agents.admin

## Imports
- django.contrib
- models

## Classes
- AgentAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
  - attr: `actions`
  - method: `activate_agents`
  - method: `deactivate_agents`
- AgentCapabilityAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
- RoleAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `readonly_fields`
- PermissionAdmin
  - attr: `list_display`
  - attr: `search_fields`
- RolePermissionAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
- UserRoleAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- AgentRoleAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- MessageAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`

## Functions
- activate_agents
- deactivate_agents

## Class Diagram

```mermaid
classDiagram
    class AgentAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
        +actions
        +activate_agents()
        +deactivate_agents()
    }
    class AgentCapabilityAdmin {
        +list_display
        +list_filter
        +search_fields
    }
    class RoleAdmin {
        +list_display
        +search_fields
        +readonly_fields
    }
    class PermissionAdmin {
        +list_display
        +search_fields
    }
    class RolePermissionAdmin {
        +list_display
        +list_filter
        +search_fields
    }
    class UserRoleAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class AgentRoleAdmin {
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
