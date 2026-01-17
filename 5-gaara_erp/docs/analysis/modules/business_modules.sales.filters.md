# business_modules.sales.filters

## Imports
- django.utils.translation
- django_filters
- models

## Classes
- CustomerProfileFilter
  - attr: `contact_name`
  - attr: `contact_email`
  - attr: `contact_phone`
  - attr: `salesperson`
- SalesDocumentFilter
  - attr: `customer`
  - attr: `customer_name`
  - attr: `created_by`
  - attr: `start_date`
  - attr: `end_date`
- SalesQuotationFilter
  - attr: `quotation_id`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `expiry_start_date`
  - attr: `expiry_end_date`
- SalesOrderFilter
  - attr: `order_id`
  - attr: `quotation_id`
  - attr: `start_date`
  - attr: `end_date`
- DeliveryNoteFilter
  - attr: `delivery_note_id`
  - attr: `sales_order_id`
  - attr: `store`
  - attr: `start_date`
  - attr: `end_date`
- SalesInvoiceFilter
  - attr: `invoice_id`
  - attr: `sales_order_id`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `due_start_date`
  - attr: `due_end_date`
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
    class CustomerProfileFilter {
        +contact_name
        +contact_email
        +contact_phone
        +salesperson
    }
    class SalesDocumentFilter {
        +customer
        +customer_name
        +created_by
        +start_date
        +end_date
    }
    class SalesQuotationFilter {
        +quotation_id
        +start_date
        +end_date
        +expiry_start_date
        +expiry_end_date
    }
    class SalesOrderFilter {
        +order_id
        +quotation_id
        +start_date
        +end_date
    }
    class DeliveryNoteFilter {
        +delivery_note_id
        +sales_order_id
        +store
        +start_date
        +end_date
    }
    class SalesInvoiceFilter {
        +invoice_id
        +sales_order_id
        +start_date
        +end_date
        +due_start_date
        +... (1 more)
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
    CustomerProfileFilter --> Meta
    CustomerProfileFilter --> Meta
    CustomerProfileFilter --> Meta
    CustomerProfileFilter --> Meta
    CustomerProfileFilter --> Meta
    CustomerProfileFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesDocumentFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesQuotationFilter --> Meta
    SalesOrderFilter --> Meta
    SalesOrderFilter --> Meta
    SalesOrderFilter --> Meta
    SalesOrderFilter --> Meta
    SalesOrderFilter --> Meta
    SalesOrderFilter --> Meta
    DeliveryNoteFilter --> Meta
    DeliveryNoteFilter --> Meta
    DeliveryNoteFilter --> Meta
    DeliveryNoteFilter --> Meta
    DeliveryNoteFilter --> Meta
    DeliveryNoteFilter --> Meta
    SalesInvoiceFilter --> Meta
    SalesInvoiceFilter --> Meta
    SalesInvoiceFilter --> Meta
    SalesInvoiceFilter --> Meta
    SalesInvoiceFilter --> Meta
    SalesInvoiceFilter --> Meta
```
