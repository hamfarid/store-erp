# services_modules.workflows.models.workflow_conditional

## Imports
- django.contrib.auth
- django.db
- django.utils.translation
- json

## Classes
- ConditionalBranch
  - attr: `OPERATOR_CHOICES`
  - attr: `workflow`
  - attr: `name`
  - attr: `description`
  - attr: `source_action`
  - attr: `condition_field`
  - attr: `condition_operator`
  - attr: `condition_value`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `evaluate_condition`
- ConditionalBranchTarget
  - attr: `branch`
  - attr: `target_action`
  - attr: `condition_result`
  - attr: `order`
  - method: `__str__`
- ConditionalBranchExecution
  - attr: `branch`
  - attr: `workflow_execution`
  - attr: `condition_result`
  - attr: `context_data`
  - attr: `executed_at`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`
  - attr: `app_label`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `app_label`

## Functions
- __str__
- evaluate_condition
- __str__
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class ConditionalBranch {
        +OPERATOR_CHOICES
        +workflow
        +name
        +description
        +source_action
        +... (6 more)
        +__str__()
        +evaluate_condition()
    }
    class ConditionalBranchTarget {
        +branch
        +target_action
        +condition_result
        +order
        +__str__()
    }
    class ConditionalBranchExecution {
        +branch
        +workflow_execution
        +condition_result
        +context_data
        +executed_at
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
        +app_label
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +app_label
    }
    ConditionalBranch --> Meta
    ConditionalBranch --> Meta
    ConditionalBranch --> Meta
    ConditionalBranchTarget --> Meta
    ConditionalBranchTarget --> Meta
    ConditionalBranchTarget --> Meta
    ConditionalBranchExecution --> Meta
    ConditionalBranchExecution --> Meta
    ConditionalBranchExecution --> Meta
```
