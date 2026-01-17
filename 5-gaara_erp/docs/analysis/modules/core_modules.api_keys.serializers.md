# core_modules.api_keys.serializers

## Imports
- models
- rest_framework

## Classes
- APIKeySerializer
- APIKeyLogSerializer
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
    class APIKeySerializer {
    }
    class APIKeyLogSerializer {
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
    APIKeySerializer --> Meta
    APIKeySerializer --> Meta
    APIKeyLogSerializer --> Meta
    APIKeyLogSerializer --> Meta
```
