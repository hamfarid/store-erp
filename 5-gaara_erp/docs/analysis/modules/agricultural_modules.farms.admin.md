# agricultural_modules.farms.admin

## Imports
- django.contrib
- models

## Classes
- FarmAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- PlotAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- CropAdmin
  - attr: `list_display`
  - attr: `search_fields`
  - attr: `readonly_fields`
- PlantingAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`
- FarmActivityAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`
- HarvestAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`
- EquipmentAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `readonly_fields`
- EquipmentMaintenanceAdmin
  - attr: `list_display`
  - attr: `list_filter`
  - attr: `search_fields`
  - attr: `date_hierarchy`
  - attr: `readonly_fields`

## Class Diagram

```mermaid
classDiagram
    class FarmAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class PlotAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class CropAdmin {
        +list_display
        +search_fields
        +readonly_fields
    }
    class PlantingAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +readonly_fields
    }
    class FarmActivityAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +readonly_fields
    }
    class HarvestAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +readonly_fields
    }
    class EquipmentAdmin {
        +list_display
        +list_filter
        +search_fields
        +readonly_fields
    }
    class EquipmentMaintenanceAdmin {
        +list_display
        +list_filter
        +search_fields
        +date_hierarchy
        +readonly_fields
    }
```
