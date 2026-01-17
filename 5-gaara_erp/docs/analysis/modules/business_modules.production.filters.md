# business_modules.production.filters

## Imports
- django.db
- django_filters
- models

## Classes
- BillOfMaterialsFilter
  - attr: `name`
- BOMComponentFilter
- ManufacturingOrderFilter
  - attr: `name`
  - attr: `scheduled_start_date`
  - attr: `scheduled_end_date`
  - attr: `actual_start_date`
  - attr: `actual_end_date`
- WorkOrderFilter
  - attr: `name`
  - attr: `scheduled_start_date`
  - attr: `actual_start_date`
- WorkCenterFilter
  - attr: `name`
  - attr: `code`
- RoutingFilter
  - attr: `name`
- RoutingOperationFilter
  - attr: `name`
- ProductionLogFilter
  - attr: `timestamp`
  - attr: `log_type`
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
    class BillOfMaterialsFilter {
        +name
    }
    class BOMComponentFilter {
    }
    class ManufacturingOrderFilter {
        +name
        +scheduled_start_date
        +scheduled_end_date
        +actual_start_date
        +actual_end_date
    }
    class WorkOrderFilter {
        +name
        +scheduled_start_date
        +actual_start_date
    }
    class WorkCenterFilter {
        +name
        +code
    }
    class RoutingFilter {
        +name
    }
    class RoutingOperationFilter {
        +name
    }
    class ProductionLogFilter {
        +timestamp
        +log_type
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
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BillOfMaterialsFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    BOMComponentFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    ManufacturingOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkOrderFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    WorkCenterFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    RoutingOperationFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
    ProductionLogFilter --> Meta
```
