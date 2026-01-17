# business_modules.inventory.products

## Imports
- decimal
- django.db
- django.utils.translation
- models

## Classes
- ProductAttribute
  - attr: `DISPLAY_CHOICES`
  - attr: `name`
  - attr: `description`
  - attr: `display_type`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- ProductAttributeValue
  - attr: `attribute`
  - attr: `name`
  - attr: `html_color`
  - attr: `sequence`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- ProductVariant
  - attr: `product`
  - attr: `name`
  - attr: `sku`
  - attr: `barcode`
  - attr: `attribute_values`
  - attr: `sale_price`
  - attr: `cost_price`
  - attr: `quantity_on_hand`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- SupplierProduct
  - attr: `product`
  - attr: `supplier_id`
  - attr: `supplier_name`
  - attr: `supplier_product_code`
  - attr: `supplier_product_name`
  - attr: `purchase_price`
  - attr: `purchase_uom`
  - attr: `min_order_qty`
  - attr: `lead_time_days`
  - attr: `is_preferred`
  - attr: `notes`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- UOMConversion
  - attr: `product`
  - attr: `from_uom`
  - attr: `to_uom`
  - attr: `factor`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class ProductAttribute {
        +DISPLAY_CHOICES
        +name
        +description
        +display_type
        +is_active
        +... (2 more)
        +__str__()
    }
    class ProductAttributeValue {
        +attribute
        +name
        +html_color
        +sequence
        +is_active
        +... (2 more)
        +__str__()
    }
    class ProductVariant {
        +product
        +name
        +sku
        +barcode
        +attribute_values
        +... (6 more)
        +__str__()
    }
    class SupplierProduct {
        +product
        +supplier_id
        +supplier_name
        +supplier_product_code
        +supplier_product_name
        +... (9 more)
        +__str__()
    }
    class UOMConversion {
        +product
        +from_uom
        +to_uom
        +factor
        +is_active
        +... (2 more)
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    ProductAttribute --> Meta
    ProductAttribute --> Meta
    ProductAttribute --> Meta
    ProductAttribute --> Meta
    ProductAttribute --> Meta
    ProductAttributeValue --> Meta
    ProductAttributeValue --> Meta
    ProductAttributeValue --> Meta
    ProductAttributeValue --> Meta
    ProductAttributeValue --> Meta
    ProductVariant --> Meta
    ProductVariant --> Meta
    ProductVariant --> Meta
    ProductVariant --> Meta
    ProductVariant --> Meta
    SupplierProduct --> Meta
    SupplierProduct --> Meta
    SupplierProduct --> Meta
    SupplierProduct --> Meta
    SupplierProduct --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
    UOMConversion --> Meta
```
