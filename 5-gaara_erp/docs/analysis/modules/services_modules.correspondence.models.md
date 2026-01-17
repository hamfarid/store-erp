# services_modules.correspondence.models

## Imports
- django.conf
- django.db
- django.utils
- django.utils.translation

## Classes
- CorrespondenceCategory
  - attr: `name`
  - attr: `code`
  - attr: `description`
  - attr: `is_active`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- Correspondence
  - attr: `subject`
  - attr: `content`
  - attr: `reference_number`
  - attr: `date`
  - attr: `correspondence_type`
  - attr: `status`
  - attr: `priority`
  - attr: `category`
  - attr: `tags`
  - attr: `is_confidential`
  - attr: `is_archived`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `save`
- CorrespondenceAttachment
  - attr: `correspondence`
  - attr: `name`
  - attr: `file`
  - attr: `description`
  - attr: `uploaded_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `save`
- CorrespondenceComment
  - attr: `correspondence`
  - attr: `content`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- CorrespondenceHistory
  - attr: `correspondence`
  - attr: `action`
  - attr: `description`
  - attr: `performed_by`
  - attr: `performed_at`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- CorrespondenceType
  - attr: `INCOMING`
  - attr: `OUTGOING`
  - attr: `INTERNAL`
- CorrespondenceStatus
  - attr: `NEW`
  - attr: `IN_PROGRESS`
  - attr: `COMPLETED`
  - attr: `CANCELLED`
  - attr: `ON_HOLD`
- CorrespondencePriority
  - attr: `LOW`
  - attr: `NORMAL`
  - attr: `HIGH`
  - attr: `URGENT`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `permissions`
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
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- save
- __str__
- save
- __str__
- __str__

## Module Variables
- `CorrespondenceType`
- `CorrespondenceStatus`
- `CorrespondencePriority`

## Class Diagram

```mermaid
classDiagram
    class CorrespondenceCategory {
        +name
        +code
        +description
        +is_active
        +created_at
        +... (1 more)
        +__str__()
    }
    class Correspondence {
        +subject
        +content
        +reference_number
        +date
        +correspondence_type
        +... (9 more)
        +__str__()
        +save()
    }
    class CorrespondenceAttachment {
        +correspondence
        +name
        +file
        +description
        +uploaded_by
        +... (2 more)
        +__str__()
        +save()
    }
    class CorrespondenceComment {
        +correspondence
        +content
        +created_by
        +created_at
        +updated_at
        +__str__()
    }
    class CorrespondenceHistory {
        +correspondence
        +action
        +description
        +performed_by
        +performed_at
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class CorrespondenceType {
        +INCOMING
        +OUTGOING
        +INTERNAL
    }
    class CorrespondenceStatus {
        +NEW
        +IN_PROGRESS
        +COMPLETED
        +CANCELLED
        +ON_HOLD
    }
    class CorrespondencePriority {
        +LOW
        +NORMAL
        +HIGH
        +URGENT
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +permissions
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
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    CorrespondenceCategory --> Meta
    CorrespondenceCategory --> Meta
    CorrespondenceCategory --> Meta
    CorrespondenceCategory --> Meta
    CorrespondenceCategory --> Meta
    Correspondence --> Meta
    Correspondence --> Meta
    Correspondence --> Meta
    Correspondence --> Meta
    Correspondence --> Meta
    CorrespondenceAttachment --> Meta
    CorrespondenceAttachment --> Meta
    CorrespondenceAttachment --> Meta
    CorrespondenceAttachment --> Meta
    CorrespondenceAttachment --> Meta
    CorrespondenceComment --> Meta
    CorrespondenceComment --> Meta
    CorrespondenceComment --> Meta
    CorrespondenceComment --> Meta
    CorrespondenceComment --> Meta
    CorrespondenceHistory --> Meta
    CorrespondenceHistory --> Meta
    CorrespondenceHistory --> Meta
    CorrespondenceHistory --> Meta
    CorrespondenceHistory --> Meta
    CorrespondenceType --> Meta
    CorrespondenceType --> Meta
    CorrespondenceType --> Meta
    CorrespondenceType --> Meta
    CorrespondenceType --> Meta
    CorrespondenceStatus --> Meta
    CorrespondenceStatus --> Meta
    CorrespondenceStatus --> Meta
    CorrespondenceStatus --> Meta
    CorrespondenceStatus --> Meta
    CorrespondencePriority --> Meta
    CorrespondencePriority --> Meta
    CorrespondencePriority --> Meta
    CorrespondencePriority --> Meta
    CorrespondencePriority --> Meta
```
