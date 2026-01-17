# services_modules.correspondence.serializers

## Imports
- django.contrib.auth
- django.utils.translation
- models
- rest_framework

## Classes
- UserSerializer
- CorrespondenceCategorySerializer
- CorrespondenceAttachmentSerializer
  - attr: `uploaded_by`
- CorrespondenceCommentSerializer
  - attr: `created_by`
- CorrespondenceHistorySerializer
  - attr: `performed_by`
- CorrespondenceSerializer
  - attr: `created_by`
  - attr: `category`
  - attr: `category_id`
  - attr: `correspondence_type_display`
  - attr: `status_display`
  - attr: `priority_display`
  - attr: `attachments_count`
  - attr: `comments_count`
  - method: `get_correspondence_type_display`
  - method: `get_status_display`
  - method: `get_priority_display`
  - method: `get_attachments_count`
  - method: `get_comments_count`
  - method: `validate_reference_number`
  - method: `validate`
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
- get_correspondence_type_display
- get_status_display
- get_priority_display
- get_attachments_count
- get_comments_count
- validate_reference_number
- validate

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserSerializer {
    }
    class CorrespondenceCategorySerializer {
    }
    class CorrespondenceAttachmentSerializer {
        +uploaded_by
    }
    class CorrespondenceCommentSerializer {
        +created_by
    }
    class CorrespondenceHistorySerializer {
        +performed_by
    }
    class CorrespondenceSerializer {
        +created_by
        +category
        +category_id
        +correspondence_type_display
        +status_display
        +... (3 more)
        +get_correspondence_type_display()
        +get_status_display()
        +get_priority_display()
        +get_attachments_count()
        +get_comments_count()
        +... (2 more)
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
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceCategorySerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceAttachmentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceCommentSerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceHistorySerializer --> Meta
    CorrespondenceSerializer --> Meta
    CorrespondenceSerializer --> Meta
    CorrespondenceSerializer --> Meta
    CorrespondenceSerializer --> Meta
    CorrespondenceSerializer --> Meta
    CorrespondenceSerializer --> Meta
```
