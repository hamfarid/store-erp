# services_modules.projects.models.project

## Imports
- core_modules.organization.models
- django.contrib.auth
- django.core.exceptions
- django.db
- django.utils.translation

## Classes
- Project
  - attr: `STATUS_CHOICES`
  - attr: `PRIORITY_CHOICES`
  - attr: `name`
  - attr: `code`
  - attr: `description`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `actual_start_date`
  - attr: `actual_end_date`
  - attr: `status`
  - attr: `priority`
  - attr: `budget`
  - attr: `owner`
  - attr: `company`
  - attr: `currency`
  - attr: `workflow`
  - attr: `workflow_step`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- ProjectCategory
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `description`
  - attr: `is_active`
  - method: `__str__`
- ProjectStatus
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `description`
  - attr: `is_active`
  - method: `__str__`
- ProjectTag
  - attr: `name`
  - attr: `code`
  - attr: `company`
  - attr: `color`
  - attr: `is_active`
  - method: `__str__`
- ProjectTask
  - attr: `STATUS_CHOICES`
  - attr: `PRIORITY_CHOICES`
  - attr: `project`
  - attr: `phase`
  - attr: `title`
  - attr: `description`
  - attr: `status`
  - attr: `priority`
  - attr: `assignee`
  - attr: `reporter`
  - attr: `due_date`
  - attr: `estimated_hours`
  - attr: `actual_hours`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `parent_task`
  - attr: `created_at`
  - attr: `updated_at`
  - attr: `task`
  - method: `__str__`
- ProjectTaskDependency
  - attr: `DEPENDENCY_TYPE_CHOICES`
  - attr: `task`
  - attr: `dependency`
  - attr: `dependency_type`
  - attr: `lag_days`
  - method: `__str__`
  - method: `clean`
- ProjectDocument
  - attr: `project`
  - attr: `task`
  - attr: `name`
  - attr: `description`
  - attr: `file`
  - attr: `uploaded_by`
  - attr: `uploaded_at`
  - method: `__str__`
- ProjectRisk
  - attr: `PROBABILITY_CHOICES`
  - attr: `IMPACT_CHOICES`
  - attr: `STATUS_CHOICES`
  - attr: `project`
  - attr: `description`
  - attr: `probability`
  - attr: `impact`
  - attr: `status`
  - attr: `mitigation_plan`
  - attr: `owner`
  - attr: `identified_date`
  - attr: `resolution_date`
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
  - attr: `constraints`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `constraints`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `constraints`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
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
- __str__
- __str__
- __str__
- __str__
- clean
- __str__
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class Project {
        +STATUS_CHOICES
        +PRIORITY_CHOICES
        +name
        +code
        +description
        +... (14 more)
        +__str__()
    }
    class ProjectCategory {
        +name
        +code
        +company
        +description
        +is_active
        +__str__()
    }
    class ProjectStatus {
        +name
        +code
        +company
        +description
        +is_active
        +__str__()
    }
    class ProjectTag {
        +name
        +code
        +company
        +color
        +is_active
        +__str__()
    }
    class ProjectTask {
        +STATUS_CHOICES
        +PRIORITY_CHOICES
        +project
        +phase
        +title
        +... (14 more)
        +__str__()
    }
    class ProjectTaskDependency {
        +DEPENDENCY_TYPE_CHOICES
        +task
        +dependency
        +dependency_type
        +lag_days
        +__str__()
        +clean()
    }
    class ProjectDocument {
        +project
        +task
        +name
        +description
        +file
        +... (2 more)
        +__str__()
    }
    class ProjectRisk {
        +PROBABILITY_CHOICES
        +IMPACT_CHOICES
        +STATUS_CHOICES
        +project
        +description
        +... (7 more)
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
        +constraints
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +constraints
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +constraints
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
        +unique_together
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
    Project --> Meta
    Project --> Meta
    Project --> Meta
    Project --> Meta
    Project --> Meta
    Project --> Meta
    Project --> Meta
    Project --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectCategory --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectStatus --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTag --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTask --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectTaskDependency --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectDocument --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
    ProjectRisk --> Meta
```
