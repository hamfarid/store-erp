# admin_modules.system_backups.models

## Imports
- calendar
- django.conf
- django.core.exceptions
- django.core.validators
- django.db
- django.utils
- django.utils.translation

## Classes
- BackupConfiguration
  - attr: `STORAGE_TYPE_CHOICES`
  - attr: `CLOUD_PROVIDER_CHOICES`
  - attr: `COMPRESSION_CHOICES`
  - attr: `name`
  - attr: `description`
  - attr: `is_active`
  - attr: `is_default`
  - attr: `storage_type`
  - attr: `local_storage_path`
  - attr: `cloud_provider`
  - attr: `cloud_bucket`
  - attr: `cloud_prefix`
  - attr: `cloud_credentials`
  - attr: `compression_type`
  - attr: `encryption_enabled`
  - attr: `encryption_key`
  - attr: `retention_days`
  - attr: `max_backups`
  - attr: `notify_on_success`
  - attr: `notify_on_failure`
  - attr: `notification_emails`
  - attr: `created_at`
  - attr: `updated_at`
  - attr: `created_by`
  - method: `__str__`
  - method: `clean`
  - method: `save`
- BackupSchedule
  - attr: `FREQUENCY_CHOICES`
  - attr: `BACKUP_TYPE_CHOICES`
  - attr: `DAY_OF_WEEK_CHOICES`
  - attr: `name`
  - attr: `description`
  - attr: `configuration`
  - attr: `backup_type`
  - attr: `frequency`
  - attr: `hour`
  - attr: `minute`
  - attr: `day_of_week`
  - attr: `day_of_month`
  - attr: `cron_expression`
  - attr: `is_active`
  - attr: `last_run`
  - attr: `next_run`
  - attr: `created_at`
  - attr: `updated_at`
  - attr: `created_by`
  - method: `__str__`
  - method: `clean`
  - method: `calculate_next_run`
  - method: `save`
- BackupLog
  - attr: `BACKUP_TYPE_CHOICES`
  - attr: `TRIGGER_TYPE_CHOICES`
  - attr: `STATUS_CHOICES`
  - attr: `STORAGE_LOCATION_CHOICES`
  - attr: `name`
  - attr: `configuration`
  - attr: `schedule`
  - attr: `backup_type`
  - attr: `trigger_type`
  - attr: `status`
  - attr: `storage_location`
  - attr: `started_at`
  - attr: `completed_at`
  - attr: `duration_seconds`
  - attr: `local_path`
  - attr: `cloud_url`
  - attr: `file_size`
  - attr: `message`
  - attr: `is_encrypted`
  - attr: `is_compressed`
  - attr: `compression_type`
  - attr: `expiry_date`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `file_size_human_readable`
  - method: `save`
- RestoreLog
  - attr: `STATUS_CHOICES`
  - attr: `RESTORE_TYPE_CHOICES`
  - attr: `TRIGGER_TYPE_CHOICES`
  - attr: `name`
  - attr: `source_backup`
  - attr: `restore_type`
  - attr: `trigger_type`
  - attr: `status`
  - attr: `started_at`
  - attr: `completed_at`
  - attr: `duration_seconds`
  - attr: `message`
  - attr: `is_overwrite`
  - attr: `created_by`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `save`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `indexes`

## Functions
- __str__
- clean
- save
- __str__
- clean
- calculate_next_run
- save
- __str__
- file_size_human_readable
- save
- __str__
- save

## Class Diagram

```mermaid
classDiagram
    class BackupConfiguration {
        +STORAGE_TYPE_CHOICES
        +CLOUD_PROVIDER_CHOICES
        +COMPRESSION_CHOICES
        +name
        +description
        +... (19 more)
        +__str__()
        +clean()
        +save()
    }
    class BackupSchedule {
        +FREQUENCY_CHOICES
        +BACKUP_TYPE_CHOICES
        +DAY_OF_WEEK_CHOICES
        +name
        +description
        +... (14 more)
        +__str__()
        +clean()
        +calculate_next_run()
        +save()
    }
    class BackupLog {
        +BACKUP_TYPE_CHOICES
        +TRIGGER_TYPE_CHOICES
        +STATUS_CHOICES
        +STORAGE_LOCATION_CHOICES
        +name
        +... (20 more)
        +__str__()
        +file_size_human_readable()
        +save()
    }
    class RestoreLog {
        +STATUS_CHOICES
        +RESTORE_TYPE_CHOICES
        +TRIGGER_TYPE_CHOICES
        +name
        +source_backup
        +... (11 more)
        +__str__()
        +save()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
        +indexes
    }
    BackupConfiguration --> Meta
    BackupConfiguration --> Meta
    BackupConfiguration --> Meta
    BackupConfiguration --> Meta
    BackupSchedule --> Meta
    BackupSchedule --> Meta
    BackupSchedule --> Meta
    BackupSchedule --> Meta
    BackupLog --> Meta
    BackupLog --> Meta
    BackupLog --> Meta
    BackupLog --> Meta
    RestoreLog --> Meta
    RestoreLog --> Meta
    RestoreLog --> Meta
    RestoreLog --> Meta
```
