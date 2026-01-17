# admin_modules.custom_admin.serializers.customization_serializers

## Imports
- models
- rest_framework

## Classes
- CustomUIElementSerializer
  - attr: `created_by_username`
- CustomReportSerializer
  - attr: `created_by_username`
- CustomMenuSerializer
  - attr: `created_by_username`
  - attr: `parent_title`
  - attr: `children`
  - method: `get_children`
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
  - attr: `fields`
  - attr: `read_only_fields`

## Functions
- get_children

## Class Diagram

```mermaid
classDiagram
    class CustomUIElementSerializer {
        +created_by_username
    }
    class CustomReportSerializer {
        +created_by_username
    }
    class CustomMenuSerializer {
        +created_by_username
        +parent_title
        +children
        +get_children()
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
        +fields
        +read_only_fields
    }
    CustomUIElementSerializer --> Meta
    CustomUIElementSerializer --> Meta
    CustomUIElementSerializer --> Meta
    CustomReportSerializer --> Meta
    CustomReportSerializer --> Meta
    CustomReportSerializer --> Meta
    CustomMenuSerializer --> Meta
    CustomMenuSerializer --> Meta
    CustomMenuSerializer --> Meta
```
