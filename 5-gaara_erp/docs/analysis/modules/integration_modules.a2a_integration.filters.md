# integration_modules.a2a_integration.filters

## Imports
- django_filters
- models

## Classes
- ExternalSystemFilter
  - attr: `name`
  - attr: `system_type`
  - attr: `is_active`
- IntegrationConfigFilter
  - attr: `name`
  - attr: `external_system`
  - attr: `integration_type`
  - attr: `direction`
  - attr: `is_active`
- APICredentialFilter
  - attr: `name`
  - attr: `external_system`
  - attr: `auth_type`
  - attr: `is_active`
- IntegrationLogFilter
  - attr: `integration_config`
  - attr: `status`
  - attr: `created_at`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Class Diagram

```mermaid
classDiagram
    class ExternalSystemFilter {
        +name
        +system_type
        +is_active
    }
    class IntegrationConfigFilter {
        +name
        +external_system
        +integration_type
        +direction
        +is_active
    }
    class APICredentialFilter {
        +name
        +external_system
        +auth_type
        +is_active
    }
    class IntegrationLogFilter {
        +integration_config
        +status
        +created_at
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    ExternalSystemFilter --> Meta
    ExternalSystemFilter --> Meta
    ExternalSystemFilter --> Meta
    ExternalSystemFilter --> Meta
    IntegrationConfigFilter --> Meta
    IntegrationConfigFilter --> Meta
    IntegrationConfigFilter --> Meta
    IntegrationConfigFilter --> Meta
    APICredentialFilter --> Meta
    APICredentialFilter --> Meta
    APICredentialFilter --> Meta
    APICredentialFilter --> Meta
    IntegrationLogFilter --> Meta
    IntegrationLogFilter --> Meta
    IntegrationLogFilter --> Meta
    IntegrationLogFilter --> Meta
```
