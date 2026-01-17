# admin_modules.internal_diagnosis_module.models

## Imports
- django.conf
- django.db
- django.utils
- django.utils.translation

## Classes
- DiagnosisSession
  - attr: `STATUS_CHOICES`
  - attr: `session_id`
  - attr: `status`
  - attr: `started_at`
  - attr: `completed_at`
  - attr: `initiated_by`
  - method: `__str__`
  - method: `duration`
- DiagnosisResult
  - attr: `SEVERITY_CHOICES`
  - attr: `session`
  - attr: `component`
  - attr: `check_name`
  - attr: `severity`
  - attr: `message`
  - attr: `details`
  - attr: `timestamp`
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

## Functions
- __str__
- duration
- __str__

## Class Diagram

```mermaid
classDiagram
    class DiagnosisSession {
        +STATUS_CHOICES
        +session_id
        +status
        +started_at
        +completed_at
        +... (1 more)
        +__str__()
        +duration()
    }
    class DiagnosisResult {
        +SEVERITY_CHOICES
        +session
        +component
        +check_name
        +severity
        +... (3 more)
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
    }
    DiagnosisSession --> Meta
    DiagnosisSession --> Meta
    DiagnosisResult --> Meta
    DiagnosisResult --> Meta
```
