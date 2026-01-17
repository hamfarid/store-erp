# services_modules.quality_control.forms

## Imports
- django
- django.core.exceptions
- django.utils
- django.utils.translation
- models

## Classes
- QualityTemplateForm
  - method: `clean_code`
- QualityParameterForm
  - method: `__init__`
  - method: `clean`
- QualityCheckForm
  - method: `__init__`
  - method: `clean_reference_number`
- QualityResultForm
  - method: `__init__`
  - method: `clean`
- QualityCertificateForm
  - method: `__init__`
  - method: `get_certificate_type_from_check`
  - method: `clean`
  - method: `clean_certificate_number`
- QualityIssueForm
  - method: `__init__`
  - method: `clean_reference_number`
- QualityImprovementForm
  - method: `__init__`
  - method: `clean_reference_number`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
  - attr: `help_texts`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `widgets`

## Functions
- clean_code
- __init__
- clean
- __init__
- clean_reference_number
- __init__
- clean
- __init__
- get_certificate_type_from_check
- clean
- clean_certificate_number
- __init__
- clean_reference_number
- __init__
- clean_reference_number

## Class Diagram

```mermaid
classDiagram
    class QualityTemplateForm {
        +clean_code()
    }
    class QualityParameterForm {
        +__init__()
        +clean()
    }
    class QualityCheckForm {
        +__init__()
        +clean_reference_number()
    }
    class QualityResultForm {
        +__init__()
        +clean()
    }
    class QualityCertificateForm {
        +__init__()
        +get_certificate_type_from_check()
        +clean()
        +clean_certificate_number()
    }
    class QualityIssueForm {
        +__init__()
        +clean_reference_number()
    }
    class QualityImprovementForm {
        +__init__()
        +clean_reference_number()
    }
    class Meta {
        +model
        +fields
        +widgets
        +help_texts
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    class Meta {
        +model
        +fields
        +widgets
    }
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityTemplateForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityParameterForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityCheckForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityResultForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityCertificateForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityIssueForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
    QualityImprovementForm --> Meta
```
