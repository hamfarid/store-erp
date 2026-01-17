# core_modules.users.filters

## Imports
- django.contrib.auth
- django.utils.translation
- django_filters
- models

## Classes
- UserFilter
  - attr: `email`
  - attr: `username`
  - attr: `first_name`
  - attr: `last_name`
  - attr: `is_active`
  - attr: `is_staff`
  - attr: `date_joined_after`
  - attr: `date_joined_before`
  - attr: `last_login_after`
  - attr: `last_login_before`
- UserProfileFilter
  - attr: `user_email`
  - attr: `user_username`
  - attr: `city`
  - attr: `country`
  - attr: `gender`
  - attr: `birth_date_after`
  - attr: `birth_date_before`
  - attr: `created_at_after`
  - attr: `created_at_before`
- UserDeviceFilter
  - attr: `user_email`
  - attr: `user_username`
  - attr: `device_name`
  - attr: `device_id`
  - attr: `device_type`
  - attr: `os_name`
  - attr: `browser_name`
  - attr: `is_active`
  - attr: `created_at_after`
  - attr: `created_at_before`
  - attr: `last_login_after`
  - attr: `last_login_before`
- UserSessionFilter
  - attr: `user_email`
  - attr: `user_username`
  - attr: `ip_address`
  - attr: `is_active`
  - attr: `login_time_after`
  - attr: `login_time_before`
  - attr: `last_activity_after`
  - attr: `last_activity_before`
  - attr: `logout_time_after`
  - attr: `logout_time_before`
- UserActivityFilter
  - attr: `user_email`
  - attr: `user_username`
  - attr: `activity_type`
  - attr: `description`
  - attr: `ip_address`
  - attr: `timestamp_after`
  - attr: `timestamp_before`
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

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserFilter {
        +email
        +username
        +first_name
        +last_name
        +is_active
        +... (5 more)
    }
    class UserProfileFilter {
        +user_email
        +user_username
        +city
        +country
        +gender
        +... (4 more)
    }
    class UserDeviceFilter {
        +user_email
        +user_username
        +device_name
        +device_id
        +device_type
        +... (7 more)
    }
    class UserSessionFilter {
        +user_email
        +user_username
        +ip_address
        +is_active
        +login_time_after
        +... (5 more)
    }
    class UserActivityFilter {
        +user_email
        +user_username
        +activity_type
        +description
        +ip_address
        +... (2 more)
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
    UserFilter --> Meta
    UserFilter --> Meta
    UserFilter --> Meta
    UserFilter --> Meta
    UserFilter --> Meta
    UserProfileFilter --> Meta
    UserProfileFilter --> Meta
    UserProfileFilter --> Meta
    UserProfileFilter --> Meta
    UserProfileFilter --> Meta
    UserDeviceFilter --> Meta
    UserDeviceFilter --> Meta
    UserDeviceFilter --> Meta
    UserDeviceFilter --> Meta
    UserDeviceFilter --> Meta
    UserSessionFilter --> Meta
    UserSessionFilter --> Meta
    UserSessionFilter --> Meta
    UserSessionFilter --> Meta
    UserSessionFilter --> Meta
    UserActivityFilter --> Meta
    UserActivityFilter --> Meta
    UserActivityFilter --> Meta
    UserActivityFilter --> Meta
    UserActivityFilter --> Meta
```
