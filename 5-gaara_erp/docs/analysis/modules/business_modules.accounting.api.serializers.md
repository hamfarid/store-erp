# business_modules.accounting.api.serializers

## Imports
- django.db
- models
- rest_framework

## Classes
- AccountSerializer
  - attr: `type_name`
  - attr: `parent_name`
  - attr: `current_balance`
- AccountTreeSerializer
  - attr: `id`
  - attr: `name`
  - attr: `code`
  - attr: `type`
  - attr: `balance`
  - attr: `is_active`
  - attr: `children`
- BalanceSheetSerializer
  - attr: `company`
  - attr: `date`
  - attr: `assets`
  - attr: `total_assets`
  - attr: `liabilities`
  - attr: `total_liabilities`
  - attr: `equity`
  - attr: `total_equity`
  - attr: `total_liabilities_equity`
- IncomeStatementSerializer
  - attr: `company`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `revenues`
  - attr: `total_revenues`
  - attr: `expenses`
  - attr: `total_expenses`
  - attr: `net_income`
- JournalSerializer
- TaxSerializer
- PaymentTermSerializer
- BankAccountSerializer
  - attr: `account_name`
  - attr: `currency_name`
- FiscalYearSerializer
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
    class AccountSerializer {
        +type_name
        +parent_name
        +current_balance
    }
    class AccountTreeSerializer {
        +id
        +name
        +code
        +type
        +balance
        +... (2 more)
    }
    class BalanceSheetSerializer {
        +company
        +date
        +assets
        +total_assets
        +liabilities
        +... (4 more)
    }
    class IncomeStatementSerializer {
        +company
        +start_date
        +end_date
        +revenues
        +total_revenues
        +... (3 more)
    }
    class JournalSerializer {
    }
    class TaxSerializer {
    }
    class PaymentTermSerializer {
    }
    class BankAccountSerializer {
        +account_name
        +currency_name
    }
    class FiscalYearSerializer {
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
    AccountSerializer --> Meta
    AccountSerializer --> Meta
    AccountSerializer --> Meta
    AccountSerializer --> Meta
    AccountSerializer --> Meta
    AccountSerializer --> Meta
    AccountTreeSerializer --> Meta
    AccountTreeSerializer --> Meta
    AccountTreeSerializer --> Meta
    AccountTreeSerializer --> Meta
    AccountTreeSerializer --> Meta
    AccountTreeSerializer --> Meta
    BalanceSheetSerializer --> Meta
    BalanceSheetSerializer --> Meta
    BalanceSheetSerializer --> Meta
    BalanceSheetSerializer --> Meta
    BalanceSheetSerializer --> Meta
    BalanceSheetSerializer --> Meta
    IncomeStatementSerializer --> Meta
    IncomeStatementSerializer --> Meta
    IncomeStatementSerializer --> Meta
    IncomeStatementSerializer --> Meta
    IncomeStatementSerializer --> Meta
    IncomeStatementSerializer --> Meta
    JournalSerializer --> Meta
    JournalSerializer --> Meta
    JournalSerializer --> Meta
    JournalSerializer --> Meta
    JournalSerializer --> Meta
    JournalSerializer --> Meta
    TaxSerializer --> Meta
    TaxSerializer --> Meta
    TaxSerializer --> Meta
    TaxSerializer --> Meta
    TaxSerializer --> Meta
    TaxSerializer --> Meta
    PaymentTermSerializer --> Meta
    PaymentTermSerializer --> Meta
    PaymentTermSerializer --> Meta
    PaymentTermSerializer --> Meta
    PaymentTermSerializer --> Meta
    PaymentTermSerializer --> Meta
    BankAccountSerializer --> Meta
    BankAccountSerializer --> Meta
    BankAccountSerializer --> Meta
    BankAccountSerializer --> Meta
    BankAccountSerializer --> Meta
    BankAccountSerializer --> Meta
    FiscalYearSerializer --> Meta
    FiscalYearSerializer --> Meta
    FiscalYearSerializer --> Meta
    FiscalYearSerializer --> Meta
    FiscalYearSerializer --> Meta
    FiscalYearSerializer --> Meta
```
