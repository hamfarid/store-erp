# services_modules.projects.models.project_gantt

## Imports
- datetime
- dependencies
- django.contrib.auth
- django.db
- django.utils
- django.utils.translation
- networkx
- project
- services_modules.tasks.models.task

## Classes
- ProjectSchedule
  - attr: `project`
  - attr: `name`
  - attr: `description`
  - attr: `schedule_type`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `working_days`
  - attr: `working_hours_per_day`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `get_working_days_list`
  - method: `is_working_day`
  - method: `add_working_days`
  - method: `subtract_working_days`
  - method: `get_working_days_between`
  - method: `calculate_critical_path`
- TaskSchedule
  - attr: `task`
  - attr: `earliest_start_date`
  - attr: `earliest_finish_date`
  - attr: `latest_start_date`
  - attr: `latest_finish_date`
  - attr: `actual_start_date`
  - attr: `actual_finish_date`
  - attr: `baseline_start_date`
  - attr: `baseline_finish_date`
  - attr: `slack`
  - attr: `is_critical`
  - attr: `progress_percentage`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `update_progress`
- GanttSettings
  - attr: `project`
  - attr: `show_critical_path`
  - attr: `show_baseline`
  - attr: `show_progress`
  - attr: `show_dependencies`
  - attr: `show_resources`
  - attr: `show_milestones`
  - attr: `zoom_level`
  - attr: `color_scheme`
  - attr: `custom_settings`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- GanttSnapshot
  - attr: `project`
  - attr: `name`
  - attr: `description`
  - attr: `snapshot_data`
  - attr: `created_by`
  - attr: `created_at`
  - method: `__str__`
- ScheduleTypes
  - attr: `STANDARD`
  - attr: `AGILE`
  - attr: `CRITICAL_PATH`
  - attr: `RESOURCE_LEVELED`
  - attr: `CUSTOM`
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
- ZoomLevel
  - attr: `DAY`
  - attr: `WEEK`
  - attr: `MONTH`
  - attr: `QUARTER`
  - attr: `YEAR`
- ColorScheme
  - attr: `DEFAULT`
  - attr: `STATUS`
  - attr: `PRIORITY`
  - attr: `ASSIGNEE`
  - attr: `CUSTOM`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- get_working_days_list
- is_working_day
- add_working_days
- subtract_working_days
- get_working_days_between
- calculate_critical_path
- __str__
- update_progress
- __str__
- __str__

## Module Variables
- `User`
- `__all__`

## Class Diagram

```mermaid
classDiagram
    class ProjectSchedule {
        +project
        +name
        +description
        +schedule_type
        +start_date
        +... (6 more)
        +__str__()
        +get_working_days_list()
        +is_working_day()
        +add_working_days()
        +subtract_working_days()
        +... (2 more)
    }
    class TaskSchedule {
        +task
        +earliest_start_date
        +earliest_finish_date
        +latest_start_date
        +latest_finish_date
        +... (9 more)
        +__str__()
        +update_progress()
    }
    class GanttSettings {
        +project
        +show_critical_path
        +show_baseline
        +show_progress
        +show_dependencies
        +... (7 more)
        +__str__()
    }
    class GanttSnapshot {
        +project
        +name
        +description
        +snapshot_data
        +created_by
        +... (1 more)
        +__str__()
    }
    class ScheduleTypes {
        +STANDARD
        +AGILE
        +CRITICAL_PATH
        +RESOURCE_LEVELED
        +CUSTOM
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
    class ZoomLevel {
        +DAY
        +WEEK
        +MONTH
        +QUARTER
        +YEAR
    }
    class ColorScheme {
        +DEFAULT
        +STATUS
        +PRIORITY
        +ASSIGNEE
        +CUSTOM
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    ProjectSchedule --> Meta
    ProjectSchedule --> Meta
    ProjectSchedule --> Meta
    ProjectSchedule --> Meta
    TaskSchedule --> Meta
    TaskSchedule --> Meta
    TaskSchedule --> Meta
    TaskSchedule --> Meta
    GanttSettings --> Meta
    GanttSettings --> Meta
    GanttSettings --> Meta
    GanttSettings --> Meta
    GanttSnapshot --> Meta
    GanttSnapshot --> Meta
    GanttSnapshot --> Meta
    GanttSnapshot --> Meta
    ScheduleTypes --> Meta
    ScheduleTypes --> Meta
    ScheduleTypes --> Meta
    ScheduleTypes --> Meta
    ZoomLevel --> Meta
    ZoomLevel --> Meta
    ZoomLevel --> Meta
    ZoomLevel --> Meta
    ColorScheme --> Meta
    ColorScheme --> Meta
    ColorScheme --> Meta
    ColorScheme --> Meta
```
