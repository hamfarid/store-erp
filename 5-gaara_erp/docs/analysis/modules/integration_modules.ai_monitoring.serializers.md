# integration_modules.ai_monitoring.serializers

## Imports
- models
- rest_framework

## Classes
- SecurityEventSerializer
- PerformanceAnomalySerializer
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class SecurityEventSerializer {
    }
    class PerformanceAnomalySerializer {
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    SecurityEventSerializer --> Meta
    SecurityEventSerializer --> Meta
    PerformanceAnomalySerializer --> Meta
    PerformanceAnomalySerializer --> Meta
```
