# services_modules.projects.serializers

## Imports
- django.contrib.auth.models
- django.db
- models
- rest_framework

## Classes
- UserSerializer
- ProjectCategorySerializer
- ProjectStatusSerializer
- ProjectSerializer
  - attr: `category`
  - attr: `category_id`
  - attr: `status`
  - attr: `status_id`
  - attr: `manager`
  - attr: `manager_id`
  - attr: `created_by`
  - attr: `created_by_id`
- ProjectMemberSerializer
  - attr: `project`
  - attr: `project_id`
  - attr: `user`
  - attr: `user_id`
  - attr: `added_by`
  - attr: `added_by_id`
- ProjectTaskSerializer
  - attr: `project`
  - attr: `project_id`
  - attr: `assigned_to`
  - attr: `assigned_to_id`
  - attr: `created_by`
  - attr: `created_by_id`
- ProjectDocumentSerializer
  - attr: `project`
  - attr: `project_id`
  - attr: `uploaded_by`
  - attr: `uploaded_by_id`
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
- Meta
  - attr: `model`
  - attr: `fields`

## Class Diagram

```mermaid
classDiagram
    class UserSerializer {
    }
    class ProjectCategorySerializer {
    }
    class ProjectStatusSerializer {
    }
    class ProjectSerializer {
        +category
        +category_id
        +status
        +status_id
        +manager
        +... (3 more)
    }
    class ProjectMemberSerializer {
        +project
        +project_id
        +user
        +user_id
        +added_by
        +... (1 more)
    }
    class ProjectTaskSerializer {
        +project
        +project_id
        +assigned_to
        +assigned_to_id
        +created_by
        +... (1 more)
    }
    class ProjectDocumentSerializer {
        +project
        +project_id
        +uploaded_by
        +uploaded_by_id
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
    class Meta {
        +model
        +fields
    }
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectCategorySerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectStatusSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectMemberSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectTaskSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
    ProjectDocumentSerializer --> Meta
```
