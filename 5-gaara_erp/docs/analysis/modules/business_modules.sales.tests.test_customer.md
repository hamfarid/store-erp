# business_modules.sales.tests.test_customer

## Imports
- business_modules.accounting.models
- core_modules.core.models
- decimal
- django.core.exceptions
- django.db
- django.test
- models.customer

## Classes
- CustomerModelTest
  - method: `setUp`
  - method: `test_create_customer`
  - method: `test_unique_code_per_company`
  - method: `test_customer_category`
  - method: `test_customer_tags`
  - method: `test_get_balance`
  - method: `test_get_credit_available`
  - method: `test_is_credit_limit_exceeded`
- CustomerCategoryModelTest
  - method: `setUp`
  - method: `test_create_category`
  - method: `test_unique_code_per_company`
  - method: `test_category_hierarchy`
- CustomerTagModelTest
  - method: `setUp`
  - method: `test_create_tag`
  - method: `test_unique_name_per_company`
  - method: `test_default_color`

## Functions
- setUp
- test_create_customer
- test_unique_code_per_company
- test_customer_category
- test_customer_tags
- test_get_balance
- test_get_credit_available
- test_is_credit_limit_exceeded
- setUp
- test_create_category
- test_unique_code_per_company
- test_category_hierarchy
- setUp
- test_create_tag
- test_unique_name_per_company
- test_default_color
- mock_get_balance
- mock_get_balance
- mock_get_balance
- mock_get_balance2

## Class Diagram

```mermaid
classDiagram
    class CustomerModelTest {
        +setUp()
        +test_create_customer()
        +test_unique_code_per_company()
        +test_customer_category()
        +test_customer_tags()
        +... (3 more)
    }
    class CustomerCategoryModelTest {
        +setUp()
        +test_create_category()
        +test_unique_code_per_company()
        +test_category_hierarchy()
    }
    class CustomerTagModelTest {
        +setUp()
        +test_create_tag()
        +test_unique_name_per_company()
        +test_default_color()
    }
```
