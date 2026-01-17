# integration_modules.a2a_integration.serializers

## Imports
- models
- rest_framework

## Classes
- ExternalSystemSerializer
- IntegrationConfigSerializer
  - attr: `external_system_name`
- APICredentialSerializer
  - attr: `external_system_name`
  - attr: `is_token_valid`
- IntegrationLogSerializer
  - attr: `integration_config_name`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class ExternalSystemSerializer {
    }
    class IntegrationConfigSerializer {
        +external_system_name
    }
    class APICredentialSerializer {
        +external_system_name
        +is_token_valid
    }
    class IntegrationLogSerializer {
        +integration_config_name
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
    class Meta {
        +model
        +exclude
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    ExternalSystemSerializer --> Meta
    ExternalSystemSerializer --> Meta
    ExternalSystemSerializer --> Meta
    ExternalSystemSerializer --> Meta
    IntegrationConfigSerializer --> Meta
    IntegrationConfigSerializer --> Meta
    IntegrationConfigSerializer --> Meta
    IntegrationConfigSerializer --> Meta
    APICredentialSerializer --> Meta
    APICredentialSerializer --> Meta
    APICredentialSerializer --> Meta
    APICredentialSerializer --> Meta
    IntegrationLogSerializer --> Meta
    IntegrationLogSerializer --> Meta
    IntegrationLogSerializer --> Meta
    IntegrationLogSerializer --> Meta
```
