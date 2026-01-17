# agricultural_modules.nurseries.admin

## Imports
- django.contrib
- models

## Classes
- NurseryAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- NurserySectionAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- PlantVarietyAdmin
  - attr: `list_display`
  - attr: `search_fields`
- ProductionBatchAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
  - attr: `date_hierarchy`
- BatchStageLogAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
  - attr: `date_hierarchy`
- NurseryActivityAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
  - attr: `date_hierarchy`
- NurseryResourceAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- ActivityResourceUsageAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
- QualityCheckAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
  - attr: `date_hierarchy`
- EnvironmentalLogAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `list_filter`
  - attr: `date_hierarchy`

## Class Diagram

```mermaid
classDiagram
    class NurseryAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class NurserySectionAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class PlantVarietyAdmin {
        +list_display
        +search_fields
    }
    class ProductionBatchAdmin {
        +list_display
        +search_fields
        +list_filter
        +date_hierarchy
    }
    class BatchStageLogAdmin {
        +list_display
        +search_fields
        +list_filter
        +date_hierarchy
    }
    class NurseryActivityAdmin {
        +list_display
        +search_fields
        +list_filter
        +date_hierarchy
    }
    class NurseryResourceAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class ActivityResourceUsageAdmin {
        +list_display
        +search_fields
        +list_filter
    }
    class QualityCheckAdmin {
        +list_display
        +search_fields
        +list_filter
        +date_hierarchy
    }
    class EnvironmentalLogAdmin {
        +list_display
        +search_fields
        +list_filter
        +date_hierarchy
    }
```
