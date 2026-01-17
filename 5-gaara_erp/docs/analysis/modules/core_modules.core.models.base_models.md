# core_modules.core.models.base_models

## Imports
- django.conf
- django.db
- django.utils.translation

## Classes
- TimestampedModel
  - attr: `created_at`
  - attr: `updated_at`
- UserTrackedModel
  - attr: `created_by`
  - attr: `updated_by`
- BaseModel
  - attr: `is_active`
- BaseModelWithCompany
  - attr: `company`
- Meta
  - attr: `abstract`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `abstract`
- Meta
  - attr: `abstract`
- Meta
  - attr: `abstract`
  - attr: `indexes`

## Class Diagram

```mermaid
classDiagram
    class TimestampedModel {
        +created_at
        +updated_at
    }
    class UserTrackedModel {
        +created_by
        +updated_by
    }
    class BaseModel {
        +is_active
    }
    class BaseModelWithCompany {
        +company
    }
    class Meta {
        +abstract
        +ordering
    }
    class Meta {
        +app_label
        +abstract
    }
    class Meta {
        +abstract
    }
    class Meta {
        +abstract
        +indexes
    }
    TimestampedModel --> Meta
    TimestampedModel --> Meta
    TimestampedModel --> Meta
    TimestampedModel --> Meta
    UserTrackedModel --> Meta
    UserTrackedModel --> Meta
    UserTrackedModel --> Meta
    UserTrackedModel --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    BaseModel --> Meta
    BaseModelWithCompany --> Meta
    BaseModelWithCompany --> Meta
    BaseModelWithCompany --> Meta
    BaseModelWithCompany --> Meta
```
