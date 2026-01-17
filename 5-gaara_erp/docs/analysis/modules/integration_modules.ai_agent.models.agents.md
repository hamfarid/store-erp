# integration_modules.ai_agent.models.agents

## Imports
- agent_types
- django.db
- django.utils.translation

## Classes
- Agent
  - attr: `name`
  - attr: `agent_type`
  - attr: `description`
  - attr: `is_active`
  - attr: `config`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__

## Class Diagram

```mermaid
classDiagram
    class Agent {
        +name
        +agent_type
        +description
        +is_active
        +config
        +... (2 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Agent --> Meta
```
