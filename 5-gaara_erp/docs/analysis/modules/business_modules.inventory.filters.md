# business_modules.inventory.filters

## Imports
- compat
- django.db
- django_filters
- models
- tracking

## Classes
- StoreFilter
  - attr: `name`
  - attr: `name_en`
- ProductFilter
  - attr: `name`
  - attr: `name_en`
- LotFilter
  - attr: `production_date`
  - attr: `expiry_date`
- InventoryTransactionFilter
  - attr: `transaction_date`
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
    class StoreFilter {
        +name
        +name_en
    }
    class ProductFilter {
        +name
        +name_en
    }
    class LotFilter {
        +production_date
        +expiry_date
    }
    class InventoryTransactionFilter {
        +transaction_date
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
    StoreFilter --> Meta
    StoreFilter --> Meta
    StoreFilter --> Meta
    StoreFilter --> Meta
    ProductFilter --> Meta
    ProductFilter --> Meta
    ProductFilter --> Meta
    ProductFilter --> Meta
    LotFilter --> Meta
    LotFilter --> Meta
    LotFilter --> Meta
    LotFilter --> Meta
    InventoryTransactionFilter --> Meta
    InventoryTransactionFilter --> Meta
    InventoryTransactionFilter --> Meta
    InventoryTransactionFilter --> Meta
```
