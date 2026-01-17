# services_modules.utilities.services.file_storage_service

## Imports
- django.conf
- django.core.files.base
- django.core.files.storage
- mimetypes
- models.file_storage
- os
- tempfile
- uuid

## Classes
- FileStorageService
  - method: `upload_file`
  - method: `get_file`
  - method: `get_file_content`
  - method: `delete_file`
  - method: `get_files_by_module`
  - method: `get_files_by_reference`
  - method: `create_temp_file`
  - method: `get_mime_type`
  - method: `get_file_type_from_mime`

## Functions
- upload_file
- get_file
- get_file_content
- delete_file
- get_files_by_module
- get_files_by_reference
- create_temp_file
- get_mime_type
- get_file_type_from_mime

## Class Diagram

```mermaid
classDiagram
    class FileStorageService {
        +upload_file()
        +get_file()
        +get_file_content()
        +delete_file()
        +get_files_by_module()
        +... (4 more)
    }
```
