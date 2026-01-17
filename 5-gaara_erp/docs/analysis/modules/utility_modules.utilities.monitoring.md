# utility_modules.utilities.monitoring

## Imports
- django.conf
- django.db
- django.utils.translation

## Classes
- SystemMetric
  - attr: `timestamp`
  - attr: `cpu_usage_percent`
  - attr: `memory_usage_percent`
  - attr: `disk_usage_percent`
  - method: `__str__`
- DatabaseStatus
  - attr: `timestamp`
  - attr: `database_name`
  - attr: `connection_status`
  - attr: `size_mb`
  - attr: `active_connections`
  - method: `__str__`
- UserStatistic
  - attr: `date`
  - attr: `daily_active_users`
  - attr: `weekly_active_users`
  - attr: `monthly_active_users`
  - attr: `total_users`
  - method: `__str__`
- AlertLevel
  - attr: `INFO`
  - attr: `WARNING`
  - attr: `ERROR`
  - attr: `CRITICAL`
- SystemAlert
  - attr: `timestamp`
  - attr: `level`
  - attr: `source_component`
  - attr: `message`
  - attr: `details`
  - attr: `is_resolved`
  - attr: `resolved_at`
  - attr: `resolved_by`
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
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- __str__
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class SystemMetric {
        +timestamp
        +cpu_usage_percent
        +memory_usage_percent
        +disk_usage_percent
        +__str__()
    }
    class DatabaseStatus {
        +timestamp
        +database_name
        +connection_status
        +size_mb
        +active_connections
        +__str__()
    }
    class UserStatistic {
        +date
        +daily_active_users
        +weekly_active_users
        +monthly_active_users
        +total_users
        +__str__()
    }
    class AlertLevel {
        +INFO
        +WARNING
        +ERROR
        +CRITICAL
    }
    class SystemAlert {
        +timestamp
        +level
        +source_component
        +message
        +details
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
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    SystemMetric --> Meta
    SystemMetric --> Meta
    SystemMetric --> Meta
    SystemMetric --> Meta
    DatabaseStatus --> Meta
    DatabaseStatus --> Meta
    DatabaseStatus --> Meta
    DatabaseStatus --> Meta
    UserStatistic --> Meta
    UserStatistic --> Meta
    UserStatistic --> Meta
    UserStatistic --> Meta
    AlertLevel --> Meta
    AlertLevel --> Meta
    AlertLevel --> Meta
    AlertLevel --> Meta
    SystemAlert --> Meta
    SystemAlert --> Meta
    SystemAlert --> Meta
    SystemAlert --> Meta
```
