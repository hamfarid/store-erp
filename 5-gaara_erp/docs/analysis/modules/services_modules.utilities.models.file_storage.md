# services_modules.utilities.models.file_storage

## Imports
- django.conf
- django.db
- django.urls
- django.utils.translation
- magic
- os
- uuid

## Classes
- FileStorage
  - attr: `FILE_TYPES`
  - attr: `name`
  - attr: `file`
  - attr: `file_type`
  - attr: `mime_type`
  - attr: `size`
  - attr: `description`
  - attr: `module`
  - attr: `reference_model`
  - attr: `reference_id`
  - attr: `is_public`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `save`
  - method: `get_absolute_url`
  - method: `get_file_extension`
  - method: `get_file_icon`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- file_upload_path
- __str__
- save
- get_absolute_url
- get_file_extension
- get_file_icon

## Class Diagram

```mermaid
classDiagram
    class FileStorage {
        +FILE_TYPES
        +name
        +file
        +file_type
        +mime_type
        +... (9 more)
        +__str__()
        +save()
        +get_absolute_url()
        +get_file_extension()
        +get_file_icon()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    FileStorage --> Meta
```
