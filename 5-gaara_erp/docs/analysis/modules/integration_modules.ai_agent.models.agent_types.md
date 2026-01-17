# integration_modules.ai_agent.models.agent_types

## Imports
- django.db
- django.utils.translation

## Classes
- AgentType
  - attr: `name`
  - attr: `description`
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
    class AgentType {
        +name
        +description
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    AgentType --> Meta
```
