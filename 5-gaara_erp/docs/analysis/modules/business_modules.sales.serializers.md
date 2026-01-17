# business_modules.sales.serializers

## Imports
- models
- rest_framework

## Classes
- CustomerSerializer
- SalesInvoiceItemSerializer
- SalesInvoiceSerializer
  - attr: `customer_name`
  - attr: `items`
- SalesOrderSerializer
  - attr: `customer_name`
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
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class CustomerSerializer {
    }
    class SalesInvoiceItemSerializer {
    }
    class SalesInvoiceSerializer {
        +customer_name
        +items
    }
    class SalesOrderSerializer {
        +customer_name
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
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    CustomerSerializer --> Meta
    CustomerSerializer --> Meta
    CustomerSerializer --> Meta
    CustomerSerializer --> Meta
    SalesInvoiceItemSerializer --> Meta
    SalesInvoiceItemSerializer --> Meta
    SalesInvoiceItemSerializer --> Meta
    SalesInvoiceItemSerializer --> Meta
    SalesInvoiceSerializer --> Meta
    SalesInvoiceSerializer --> Meta
    SalesInvoiceSerializer --> Meta
    SalesInvoiceSerializer --> Meta
    SalesOrderSerializer --> Meta
    SalesOrderSerializer --> Meta
    SalesOrderSerializer --> Meta
    SalesOrderSerializer --> Meta
```
