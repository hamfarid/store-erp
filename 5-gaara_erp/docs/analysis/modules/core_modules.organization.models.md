# core_modules.organization.models

## Imports
- decimal
- django.conf
- django.contrib.contenttypes.models
- django.core.exceptions
- django.core.validators
- django.db
- django.utils.translation

## Classes
- Currency
  - attr: `code`
  - attr: `name`
  - attr: `symbol`
  - attr: `decimal_places`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- ExchangeRate
  - attr: `from_currency`
  - attr: `to_currency`
  - attr: `rate`
  - attr: `date`
  - attr: `source`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Country
  - attr: `name`
  - attr: `code`
  - attr: `default_currency`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- City
  - attr: `country`
  - attr: `name`
  - attr: `code`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Company
  - attr: `name`
  - attr: `legal_name`
  - attr: `code`
  - attr: `country`
  - attr: `base_currency`
  - attr: `registration_number`
  - attr: `tax_id`
  - attr: `address`
  - attr: `phone`
  - attr: `email`
  - attr: `website`
  - attr: `logo`
  - attr: `parent_company`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Branch
  - attr: `company`
  - attr: `name`
  - attr: `code`
  - attr: `address`
  - attr: `phone`
  - attr: `email`
  - attr: `manager`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Department
  - attr: `name`
  - attr: `branch`
  - attr: `company`
  - attr: `code`
  - attr: `parent_department`
  - attr: `manager`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `clean`
  - method: `save`
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
  - attr: `unique_together`
  - attr: `ordering`
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
  - attr: `unique_together`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- __str__
- __str__
- __str__
- clean
- save
- __str__

## Class Diagram

```mermaid
classDiagram
    class Currency {
        +code
        +name
        +symbol
        +decimal_places
        +is_active
        +... (2 more)
        +__str__()
    }
    class ExchangeRate {
        +from_currency
        +to_currency
        +rate
        +date
        +source
        +... (2 more)
        +__str__()
    }
    class Country {
        +name
        +code
        +default_currency
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class City {
        +country
        +name
        +code
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class Company {
        +name
        +legal_name
        +code
        +country
        +base_currency
        +... (11 more)
        +__str__()
    }
    class Branch {
        +company
        +name
        +code
        +address
        +phone
        +... (5 more)
        +__str__()
    }
    class Department {
        +name
        +branch
        +company
        +code
        +parent_department
        +... (5 more)
        +clean()
        +save()
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
        +unique_together
        +ordering
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
        +unique_together
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Currency --> Meta
    Currency --> Meta
    Currency --> Meta
    Currency --> Meta
    Currency --> Meta
    Currency --> Meta
    Currency --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    ExchangeRate --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    Country --> Meta
    City --> Meta
    City --> Meta
    City --> Meta
    City --> Meta
    City --> Meta
    City --> Meta
    City --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Company --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Branch --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
    Department --> Meta
```
