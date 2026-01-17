# services_modules.feasibility_studies.serializers

## Imports
- django.utils.translation
- models
- rest_framework

## Classes
- CashFlowSerializer
  - method: `validate_year`
  - method: `validate`
- FeasibilityStudySerializer
  - attr: `cash_flows`
  - attr: `project`
  - attr: `project_name`
  - method: `validate_discount_rate`
  - method: `validate_initial_investment`
  - method: `validate`
  - method: `create`
  - method: `update`
- FeasibilityStudySimpleSerializer
  - attr: `project`
  - attr: `project_name`
  - attr: `cash_flows_count`
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

## Functions
- validate_year
- validate
- validate_discount_rate
- validate_initial_investment
- validate
- create
- update

## Class Diagram

```mermaid
classDiagram
    class CashFlowSerializer {
        +validate_year()
        +validate()
    }
    class FeasibilityStudySerializer {
        +cash_flows
        +project
        +project_name
        +validate_discount_rate()
        +validate_initial_investment()
        +validate()
        +create()
        +update()
    }
    class FeasibilityStudySimpleSerializer {
        +project
        +project_name
        +cash_flows_count
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
    CashFlowSerializer --> Meta
    CashFlowSerializer --> Meta
    CashFlowSerializer --> Meta
    FeasibilityStudySerializer --> Meta
    FeasibilityStudySerializer --> Meta
    FeasibilityStudySerializer --> Meta
    FeasibilityStudySimpleSerializer --> Meta
    FeasibilityStudySimpleSerializer --> Meta
    FeasibilityStudySimpleSerializer --> Meta
```
