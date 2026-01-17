# core_modules.setup.security.signals

## Imports
- activity_log.models
- django.contrib.auth
- django.contrib.auth.signals
- django.core.cache
- django.db.models.signals
- django.dispatch
- django.utils
- models

## Functions
- log_user_login
- log_user_logout
- log_user_login_failed
- log_security_event_to_activity_log
- log_blocked_ip_to_activity_log
- log_security_setting_to_activity_log
- get_client_ip
- check_brute_force_attempts

