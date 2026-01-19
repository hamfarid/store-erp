
# تقرير اختبار التكامل الشامل لنظام Gaara AI
التاريخ: 2025-07-08T04:35:37.441865

## ملخص النتائج
- إجمالي الاختبارات: 13
- نجح: 12 ✅
- فشل: 1 ❌
- تحذيرات: 0 ⚠️

## تفاصيل الاختبارات

### file_structure ✅
الحالة: PASS
الرسالة: جميع الملفات الأساسية موجودة: 18 ملف

### python_syntax ❌
الحالة: FAIL
الرسالة: أخطاء في بناء الجملة: 232 ملف
التفاصيل: {
  "syntax_errors": [
    {
      "file": "gaara_ai_integrated/backend/src/advanced_reports.py",
      "error": "invalid syntax (advanced_reports.py, line 54)",
      "line": 54
    },
    {
      "file": "gaara_ai_integrated/backend/src/advanced_security.py",
      "error": "unexpected indent (advanced_security.py, line 52)",
      "line": 52
    },
    {
      "file": "gaara_ai_integrated/backend/src/ai_insights.py",
      "error": "unindent does not match any outer indentation level (ai_insights.py, line 98)",
      "line": 98
    },
    {
      "file": "gaara_ai_integrated/backend/src/analytics_dashboard.py",
      "error": "unindent does not match any outer indentation level (analytics_dashboard.py, line 72)",
      "line": 72
    },
    {
      "file": "gaara_ai_integrated/backend/src/authentication.py",
      "error": "expected an indented block after class definition on line 45 (authentication.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/backend_enhanced.py",
      "error": "unexpected indent (backend_enhanced.py, line 87)",
      "line": 87
    },
    {
      "file": "gaara_ai_integrated/backend/src/backend_enhanced_fixed.py",
      "error": "invalid syntax. Perhaps you forgot a comma? (backend_enhanced_fixed.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/backup_system.py",
      "error": "unexpected indent (backup_system.py, line 32)",
      "line": 32
    },
    {
      "file": "gaara_ai_integrated/backend/src/caching_mixin.py",
      "error": "invalid syntax (caching_mixin.py, line 17)",
      "line": 17
    },
    {
      "file": "gaara_ai_integrated/backend/src/code_cleaner.py",
      "error": "unexpected indent (code_cleaner.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/code_inspector.py",
      "error": "unexpected indent (code_inspector.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/compliance_manager.py",
      "error": "unexpected indent (compliance_manager.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/customizable_dashboard.py",
      "error": "unindent does not match any outer indentation level (customizable_dashboard.py, line 131)",
      "line": 131
    },
    {
      "file": "gaara_ai_integrated/backend/src/dependency_fixer.py",
      "error": "unexpected indent (dependency_fixer.py, line 38)",
      "line": 38
    },
    {
      "file": "gaara_ai_integrated/backend/src/end_to_end_encryption.py",
      "error": "unindent does not match any outer indentation level (end_to_end_encryption.py, line 83)",
      "line": 83
    },
    {
      "file": "gaara_ai_integrated/backend/src/error_handler.py",
      "error": "unindent does not match any outer indentation level (error_handler.py, line 23)",
      "line": 23
    },
    {
      "file": "gaara_ai_integrated/backend/src/final_system_validator.py",
      "error": "unexpected indent (final_system_validator.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/frontend_tester.py",
      "error": "unexpected indent (frontend_tester.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/interface_integration_fixer.py",
      "error": "unexpected indent (interface_integration_fixer.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/library_compatibility_checker.py",
      "error": "unexpected indent (library_compatibility_checker.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/main.py",
      "error": "unexpected indent (main.py, line 76)",
      "line": 76
    },
    {
      "file": "gaara_ai_integrated/backend/src/memory_service.py",
      "error": "unexpected indent (memory_service.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/multilingual_system.py",
      "error": "unexpected indent (multilingual_system.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/notification_system.py",
      "error": "unexpected indent (notification_system.py, line 44)",
      "line": 44
    },
    {
      "file": "gaara_ai_integrated/backend/src/notifications_system.py",
      "error": "invalid syntax (notifications_system.py, line 57)",
      "line": 57
    },
    {
      "file": "gaara_ai_integrated/backend/src/observer.py",
      "error": "invalid syntax (observer.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/optimization.py",
      "error": "unexpected indent (optimization.py, line 21)",
      "line": 21
    },
    {
      "file": "gaara_ai_integrated/backend/src/performance_monitor.py",
      "error": "unexpected indent (performance_monitor.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/print_export_system.py",
      "error": "expected 'except' or 'finally' block (print_export_system.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/serialization_mixin.py",
      "error": "unindent does not match any outer indentation level (serialization_mixin.py, line 21)",
      "line": 21
    },
    {
      "file": "gaara_ai_integrated/backend/src/singleton.py",
      "error": "invalid syntax (singleton.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/smart_cache.py",
      "error": "unexpected indent (smart_cache.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/smart_reports.py",
      "error": "unindent does not match any outer indentation level (smart_reports.py, line 103)",
      "line": 103
    },
    {
      "file": "gaara_ai_integrated/backend/src/system_integrator.py",
      "error": "unexpected indent (system_integrator.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/type_hints_example.py",
      "error": "unexpected indent (type_hints_example.py, line 23)",
      "line": 23
    },
    {
      "file": "gaara_ai_integrated/backend/src/validation_ui_controller.py",
      "error": "invalid syntax (validation_ui_controller.py, line 27)",
      "line": 27
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_1.py",
      "error": "unexpected indent (api_1.py, line 49)",
      "line": 49
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_11.py",
      "error": "unexpected indent (api_11.py, line 88)",
      "line": 88
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_12.py",
      "error": "expected an indented block after 'try' statement on line 31 (api_12.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_14.py",
      "error": "expected an indented block after 'try' statement on line 23 (api_14.py, line 25)",
      "line": 25
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_15.py",
      "error": "unexpected indent (api_15.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_16.py",
      "error": "unexpected indent (api_16.py, line 56)",
      "line": 56
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_17.py",
      "error": "unexpected indent (api_17.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_18.py",
      "error": "unexpected indent (api_18.py, line 53)",
      "line": 53
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_19.py",
      "error": "unexpected indent (api_19.py, line 53)",
      "line": 53
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_2.py",
      "error": "unexpected indent (api_2.py, line 54)",
      "line": 54
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_20.py",
      "error": "unexpected indent (api_20.py, line 52)",
      "line": 52
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_21.py",
      "error": "unexpected indent (api_21.py, line 43)",
      "line": 43
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_23.py",
      "error": "unexpected indent (api_23.py, line 52)",
      "line": 52
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_25.py",
      "error": "invalid syntax (api_25.py, line 129)",
      "line": 129
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_27.py",
      "error": "unexpected indent (api_27.py, line 26)",
      "line": 26
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_29.py",
      "error": "unexpected indent (api_29.py, line 51)",
      "line": 51
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_3.py",
      "error": "unexpected indent (api_3.py, line 26)",
      "line": 26
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_31.py",
      "error": "unexpected indent (api_31.py, line 61)",
      "line": 61
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_32.py",
      "error": "expected an indented block after 'try' statement on line 32 (api_32.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_34.py",
      "error": "unexpected indent (api_34.py, line 55)",
      "line": 55
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_35.py",
      "error": "unexpected indent (api_35.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_36.py",
      "error": "unexpected indent (api_36.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_37.py",
      "error": "unexpected indent (api_37.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_4.py",
      "error": "unexpected indent (api_4.py, line 49)",
      "line": 49
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_5.py",
      "error": "unexpected indent (api_5.py, line 60)",
      "line": 60
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_6.py",
      "error": "unexpected indent (api_6.py, line 48)",
      "line": 48
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_7.py",
      "error": "unterminated string literal (detected at line 161) (api_7.py, line 161)",
      "line": 161
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_9.py",
      "error": "unexpected indent (api_9.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/api_security.py",
      "error": "unexpected indent (api_security.py, line 49)",
      "line": 49
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/data_api.py",
      "error": "invalid syntax (data_api.py, line 65)",
      "line": 65
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/database_api.py",
      "error": "unindent does not match any outer indentation level (database_api.py, line 69)",
      "line": 69
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/files_api.py",
      "error": "unexpected indent (files_api.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/import_export_api.py",
      "error": "unexpected indent (import_export_api.py, line 63)",
      "line": 63
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/main_api_1.py",
      "error": "unexpected indent (main_api_1.py, line 44)",
      "line": 44
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/model_comparison_api.py",
      "error": "unexpected indent (model_comparison_api.py, line 44)",
      "line": 44
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/notifications_api.py",
      "error": "unexpected indent (notifications_api.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/reports_api.py",
      "error": "unexpected indent (reports_api.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/unified_api.py",
      "error": "unexpected indent (unified_api.py, line 75)",
      "line": 75
    },
    {
      "file": "gaara_ai_integrated/backend/src/api/users_api.py",
      "error": "unexpected indent (users_api.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/base_model_backup.py",
      "error": "invalid syntax (base_model_backup.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/base_model_fixed.py",
      "error": "unindent does not match any outer indentation level (base_model_fixed.py, line 24)",
      "line": 24
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/db_models.py",
      "error": "invalid syntax (db_models.py, line 26)",
      "line": 26
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/db_models_1.py",
      "error": "did you forget parentheses around the comprehension target? (db_models_1.py, line 156)",
      "line": 156
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/db_models_2.py",
      "error": "invalid syntax (db_models_2.py, line 24)",
      "line": 24
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/db_models_permissions.py",
      "error": "invalid syntax (db_models_permissions.py, line 27)",
      "line": 27
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/model_benchmark_system.py",
      "error": "unexpected indent (model_benchmark_system.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/model_learning_system.py",
      "error": "unindent does not match any outer indentation level (model_learning_system.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/model_selector.py",
      "error": "unterminated triple-quoted string literal (detected at line 254) (model_selector.py, line 229)",
      "line": 229
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/model_validator.py",
      "error": "unexpected indent (model_validator.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models.py",
      "error": "invalid syntax (models.py, line 110)",
      "line": 110
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_1.py",
      "error": "invalid syntax (models_1.py, line 20)",
      "line": 20
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_10.py",
      "error": "invalid syntax (models_10.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_12.py",
      "error": "invalid syntax (models_12.py, line 20)",
      "line": 20
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_13.py",
      "error": "invalid syntax (models_13.py, line 18)",
      "line": 18
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_14.py",
      "error": "invalid syntax (models_14.py, line 24)",
      "line": 24
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_15.py",
      "error": "invalid syntax. Perhaps you forgot a comma? (models_15.py, line 59)",
      "line": 59
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_2.py",
      "error": "invalid syntax (models_2.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_3.py",
      "error": "invalid syntax (models_3.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_4.py",
      "error": "invalid syntax (models_4.py, line 19)",
      "line": 19
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_5.py",
      "error": "invalid syntax (models_5.py, line 23)",
      "line": 23
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_6.py",
      "error": "invalid syntax (models_6.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_7.py",
      "error": "invalid syntax (models_7.py, line 22)",
      "line": 22
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_8.py",
      "error": "invalid syntax (models_8.py, line 23)",
      "line": 23
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_9.py",
      "error": "unexpected indent (models_9.py, line 62)",
      "line": 62
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_enhanced.py",
      "error": "invalid syntax. Perhaps you forgot a comma? (models_enhanced.py, line 19)",
      "line": 19
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_enhanced_1.py",
      "error": "invalid syntax. Perhaps you forgot a comma? (models_enhanced_1.py, line 19)",
      "line": 19
    },
    {
      "file": "gaara_ai_integrated/backend/src/models/models_enhanced_2.py",
      "error": "invalid syntax. Perhaps you forgot a comma? (models_enhanced_2.py, line 19)",
      "line": 19
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/a2a_integration.py",
      "error": "unexpected indent (a2a_integration.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/a2a_integration_1.py",
      "error": "unindent does not match any outer indentation level (a2a_integration_1.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/access_control.py",
      "error": "unindent does not match any outer indentation level (access_control.py, line 38)",
      "line": 38
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/activity_integration.py",
      "error": "unexpected indent (activity_integration.py, line 63)",
      "line": 63
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/activity_log_validator.py",
      "error": "unexpected indent (activity_log_validator.py, line 39)",
      "line": 39
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/advanced_processor.py",
      "error": "invalid syntax (advanced_processor.py, line 287)",
      "line": 287
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/ai_agent_example.py",
      "error": "unexpected indent (ai_agent_example.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/ai_integration.py",
      "error": "unindent does not match any outer indentation level (ai_integration.py, line 41)",
      "line": 41
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/ai_integration_1.py",
      "error": "unexpected indent (ai_integration_1.py, line 32)",
      "line": 32
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/ai_resource_monitor.py",
      "error": "unmatched ')' (ai_resource_monitor.py, line 114)",
      "line": 114
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/ai_suspension_manager.py",
      "error": "unexpected indent (ai_suspension_manager.py, line 45)",
      "line": 45
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/alert_manager.py",
      "error": "unterminated string literal (detected at line 374) (alert_manager.py, line 374)",
      "line": 374
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/attention_analyzer.py",
      "error": "unmatched ')' (attention_analyzer.py, line 52)",
      "line": 52
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/attention_analyzer_service.py",
      "error": "unexpected indent (attention_analyzer_service.py, line 79)",
      "line": 79
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/auth_compatibility.py",
      "error": "unexpected indent (auth_compatibility.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/auth_service.py",
      "error": "invalid syntax (auth_service.py, line 47)",
      "line": 47
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/backup_service.py",
      "error": "unexpected indent (backup_service.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/backup_service_enhanced.py",
      "error": "unexpected indent (backup_service_enhanced.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/base_connector.py",
      "error": "unindent does not match any outer indentation level (base_connector.py, line 32)",
      "line": 32
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/code_validator.py",
      "error": "unexpected indent (code_validator.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config.py",
      "error": "unexpected indent (config.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config_1.py",
      "error": "unexpected indent (config_1.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config_4.py",
      "error": "'return' outside function (config_4.py, line 199)",
      "line": 199
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config_5.py",
      "error": "invalid syntax (config_5.py, line 30)",
      "line": 30
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config_6.py",
      "error": "cannot assign to function call (config_6.py, line 121)",
      "line": 121
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/config_7.py",
      "error": "invalid syntax (config_7.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/data_collector.py",
      "error": "unterminated string literal (detected at line 548) (data_collector.py, line 548)",
      "line": 548
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/data_storage.py",
      "error": "unexpected indent (data_storage.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/database_validator.py",
      "error": "invalid syntax (database_validator.py, line 41)",
      "line": 41
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/db_service.py",
      "error": "unexpected indent (db_service.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/db_service_1.py",
      "error": "unexpected indent (db_service_1.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/db_service_2.py",
      "error": "unexpected indent (db_service_2.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/decorators.py",
      "error": "unmatched ')' (decorators.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/dependencies.py",
      "error": "unexpected indent (dependencies.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/diagnosis_engine.py",
      "error": "unindent does not match any outer indentation level (diagnosis_engine.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/diagnosis_engine_enhanced.py",
      "error": "unexpected indent (diagnosis_engine_enhanced.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/disease_knowledge_base.py",
      "error": "unindent does not match any outer indentation level (disease_knowledge_base.py, line 26)",
      "line": 26
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/enhanced_knowledge_base.py",
      "error": "unexpected indent (enhanced_knowledge_base.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/error_logger.py",
      "error": "unterminated string literal (detected at line 253) (error_logger.py, line 253)",
      "line": 253
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/error_manager.py",
      "error": "unindent does not match any outer indentation level (error_manager.py, line 41)",
      "line": 41
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/error_types.py",
      "error": "unindent does not match any outer indentation level (error_types.py, line 25)",
      "line": 25
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/export_service.py",
      "error": "invalid syntax (export_service.py, line 72)",
      "line": 72
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/helpers.py",
      "error": "unexpected indent (helpers.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/hybridization_simulator.py",
      "error": "unindent does not match any outer indentation level (hybridization_simulator.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/image_collector.py",
      "error": "unexpected indent (image_collector.py, line 39)",
      "line": 39
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/image_processor.py",
      "error": "unexpected indent (image_processor.py, line 41)",
      "line": 41
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/inference_engine.py",
      "error": "unindent does not match any outer indentation level (inference_engine.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/integration.py",
      "error": "unexpected indent (integration.py, line 45)",
      "line": 45
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/integration_test.py",
      "error": "unexpected indent (integration_test.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/integration_test_1.py",
      "error": "unexpected indent (integration_test_1.py, line 45)",
      "line": 45
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/invalid_data_handler.py",
      "error": "unexpected indent (invalid_data_handler.py, line 41)",
      "line": 41
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/knowledge_base_manager.py",
      "error": "unexpected indent (knowledge_base_manager.py, line 39)",
      "line": 39
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/load_balancer.py",
      "error": "unindent does not match any outer indentation level (load_balancer.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/main.py",
      "error": "unexpected indent (main.py, line 71)",
      "line": 71
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/main_1.py",
      "error": "expected 'except' or 'finally' block (main_1.py, line 60)",
      "line": 60
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/main_2.py",
      "error": "expected 'except' or 'finally' block (main_2.py, line 61)",
      "line": 61
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_and_learning.py",
      "error": "unexpected indent (memory_and_learning.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_integration.py",
      "error": "unexpected indent (memory_integration.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_integration_1.py",
      "error": "unindent does not match any outer indentation level (memory_integration_1.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_integration_2.py",
      "error": "unindent does not match any outer indentation level (memory_integration_2.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_integration_3.py",
      "error": "unindent does not match any outer indentation level (memory_integration_3.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/memory_integration_4.py",
      "error": "unexpected indent (memory_integration_4.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/module_controller.py",
      "error": "expected an indented block after 'except' statement on line 113 (module_controller.py, line 116)",
      "line": 116
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/module_integration.py",
      "error": "unindent does not match any outer indentation level (module_integration.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/module_manager.py",
      "error": "unexpected indent (module_manager.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/monitoring_interface.py",
      "error": "unexpected indent (monitoring_interface.py, line 49)",
      "line": 49
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/performance_analyzer.py",
      "error": "expected 'except' or 'finally' block (performance_analyzer.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/performance_monitor.py",
      "error": "expected 'except' or 'finally' block (performance_monitor.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/permissions.py",
      "error": "unexpected indent (permissions.py, line 152)",
      "line": 152
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/permissions_integration.py",
      "error": "unexpected indent (permissions_integration.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/permissions_integration_1.py",
      "error": "unexpected indent (permissions_integration_1.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/priority_determiner.py",
      "error": "unexpected indent (priority_determiner.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/processor_integration.py",
      "error": "unexpected indent (processor_integration.py, line 39)",
      "line": 39
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/report_generator.py",
      "error": "unindent does not match any outer indentation level (report_generator.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/report_generator_1.py",
      "error": "expected 'except' or 'finally' block (report_generator_1.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/resource_collector.py",
      "error": "invalid syntax (resource_collector.py, line 19)",
      "line": 19
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/robustness_analyzer.py",
      "error": "unexpected indent (robustness_analyzer.py, line 32)",
      "line": 32
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/run_diagnosis.py",
      "error": "invalid syntax (run_diagnosis.py, line 42)",
      "line": 42
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/safe_shutdown_executor.py",
      "error": "unexpected indent (safe_shutdown_executor.py, line 43)",
      "line": 43
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas.py",
      "error": "unexpected indent (schemas.py, line 120)",
      "line": 120
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_10.py",
      "error": "unexpected indent (schemas_10.py, line 152)",
      "line": 152
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_11.py",
      "error": "unindent does not match any outer indentation level (schemas_11.py, line 25)",
      "line": 25
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_12.py",
      "error": "unindent does not match any outer indentation level (schemas_12.py, line 25)",
      "line": 25
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_14.py",
      "error": "unterminated string literal (detected at line 89) (schemas_14.py, line 89)",
      "line": 89
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_2.py",
      "error": "unexpected indent (schemas_2.py, line 163)",
      "line": 163
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_3.py",
      "error": "unexpected indent (schemas_3.py, line 30)",
      "line": 30
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_4.py",
      "error": "unindent does not match any outer indentation level (schemas_4.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_7.py",
      "error": "unexpected indent (schemas_7.py, line 140)",
      "line": 140
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_8.py",
      "error": "unexpected indent (schemas_8.py, line 105)",
      "line": 105
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/schemas_9.py",
      "error": "unindent does not match any outer indentation level (schemas_9.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/search_client.py",
      "error": "invalid syntax (search_client.py, line 49)",
      "line": 49
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/security.py",
      "error": "unmatched ')' (security.py, line 48)",
      "line": 48
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/security_1.py",
      "error": "unindent does not match any outer indentation level (security_1.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/security_middleware.py",
      "error": "unexpected indent (security_middleware.py, line 50)",
      "line": 50
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/security_middleware_1.py",
      "error": "unexpected indent (security_middleware_1.py, line 48)",
      "line": 48
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/security_tests.py",
      "error": "unindent does not match any outer indentation level (security_tests.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service.py",
      "error": "unexpected indent (service.py, line 44)",
      "line": 44
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_1.py",
      "error": "unexpected indent (service_1.py, line 40)",
      "line": 40
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_10.py",
      "error": "unexpected indent (service_10.py, line 37)",
      "line": 37
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_11.py",
      "error": "invalid syntax (service_11.py, line 16)",
      "line": 16
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_12.py",
      "error": "unmatched ')' (service_12.py, line 80)",
      "line": 80
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_13.py",
      "error": "unexpected indent (service_13.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_14.py",
      "error": "unindent does not match any outer indentation level (service_14.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_15.py",
      "error": "unexpected indent (service_15.py, line 28)",
      "line": 28
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_16.py",
      "error": "unexpected indent (service_16.py, line 54)",
      "line": 54
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_17.py",
      "error": "unmatched ')' (service_17.py, line 65)",
      "line": 65
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_2.py",
      "error": "invalid syntax (service_2.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_3.py",
      "error": "invalid syntax (service_3.py, line 30)",
      "line": 30
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_4.py",
      "error": "unexpected indent (service_4.py, line 46)",
      "line": 46
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_5.py",
      "error": "expected an indented block after function definition on line 49 (service_5.py, line 51)",
      "line": 51
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_6.py",
      "error": "unindent does not match any outer indentation level (service_6.py, line 33)",
      "line": 33
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_7.py",
      "error": "unexpected indent (service_7.py, line 32)",
      "line": 32
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_8.py",
      "error": "'{' was never closed (service_8.py, line 14)",
      "line": 14
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_9.py",
      "error": "unexpected indent (service_9.py, line 30)",
      "line": 30
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/service_extended.py",
      "error": "unterminated string literal (detected at line 221) (service_extended.py, line 221)",
      "line": 221
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/settings_service.py",
      "error": "unexpected indent (settings_service.py, line 39)",
      "line": 39
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/setup_wizard.py",
      "error": "unexpected indent (setup_wizard.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/storage.py",
      "error": "unindent does not match any outer indentation level (storage.py, line 27)",
      "line": 27
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/telegram.py",
      "error": "unexpected indent (telegram.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/test_integration.py",
      "error": "unexpected indent (test_integration.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/test_integration_comprehensive.py",
      "error": "unexpected indent (test_integration_comprehensive.py, line 35)",
      "line": 35
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/test_services.py",
      "error": "unexpected indent (test_services.py, line 31)",
      "line": 31
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/tests.py",
      "error": "unindent does not match any outer indentation level (tests.py, line 36)",
      "line": 36
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/url_validator.py",
      "error": "unindent does not match any outer indentation level (url_validator.py, line 30)",
      "line": 30
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/usage_analyzer.py",
      "error": "unmatched ')' (usage_analyzer.py, line 103)",
      "line": 103
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/utils.py",
      "error": "unexpected indent (utils.py, line 48)",
      "line": 48
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/validation.py",
      "error": "unexpected indent (validation.py, line 34)",
      "line": 34
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/validation_service.py",
      "error": "unterminated string literal (detected at line 65) (validation_service.py, line 65)",
      "line": 65
    },
    {
      "file": "gaara_ai_integrated/backend/src/modules/validators.py",
      "error": "unexpected indent (validators.py, line 22)",
      "line": 22
    }
  ],
  "valid_files": [
    "gaara_ai_integrated/backend/ai_diagnosis.py",
    "gaara_ai_integrated/backend/app.py",
    "gaara_ai_integrated/backend/backup_manager.py",
    "gaara_ai_integrated/backend/config.py",
    "gaara_ai_integrated/backend/database.py",
    "gaara_ai_integrated/backend/main_api.py",
    "gaara_ai_integrated/backend/models.py",
    "gaara_ai_integrated/backend/permissions.py",
    "gaara_ai_integrated/backend/routes.py",
    "gaara_ai_integrated/backend/run.py",
    "gaara_ai_integrated/backend/utils.py",
    "gaara_ai_integrated/backend/routes_complete.py",
    "gaara_ai_integrated/backend/permissions_complete.py",
    "gaara_ai_integrated/backend/controllers/__init__.py",
    "gaara_ai_integrated/backend/database/database_config.py",
    "gaara_ai_integrated/backend/database/simple_orm.py",
    "gaara_ai_integrated/backend/models/__init__.py",
    "gaara_ai_integrated/backend/services/__init__.py",
    "gaara_ai_integrated/backend/src/app.py",
    "gaara_ai_integrated/backend/src/app_1.py",
    "gaara_ai_integrated/backend/src/config.py",
    "gaara_ai_integrated/backend/src/config_1.py",
    "gaara_ai_integrated/backend/src/database_service.py",
    "gaara_ai_integrated/backend/src/wsgi.py",
    "gaara_ai_integrated/backend/src/api/api.py",
    "gaara_ai_integrated/backend/src/api/api_10.py",
    "gaara_ai_integrated/backend/src/api/api_13.py",
    "gaara_ai_integrated/backend/src/api/api_22.py",
    "gaara_ai_integrated/backend/src/api/api_24.py",
    "gaara_ai_integrated/backend/src/api/api_26.py",
    "gaara_ai_integrated/backend/src/api/api_28.py",
    "gaara_ai_integrated/backend/src/api/api_30.py",
    "gaara_ai_integrated/backend/src/api/api_33.py",
    "gaara_ai_integrated/backend/src/api/api_38.py",
    "gaara_ai_integrated/backend/src/api/api_39.py",
    "gaara_ai_integrated/backend/src/api/api_8.py",
    "gaara_ai_integrated/backend/src/api/api_permissions.py",
    "gaara_ai_integrated/backend/src/api/main_api.py",
    "gaara_ai_integrated/backend/src/models/base_model.py",
    "gaara_ai_integrated/backend/src/models/base_model_1.py",
    "gaara_ai_integrated/backend/src/models/company.py",
    "gaara_ai_integrated/backend/src/models/customer.py",
    "gaara_ai_integrated/backend/src/models/invoice.py",
    "gaara_ai_integrated/backend/src/models/models_11.py",
    "gaara_ai_integrated/backend/src/models/order.py",
    "gaara_ai_integrated/backend/src/models/product.py",
    "gaara_ai_integrated/backend/src/models/report.py",
    "gaara_ai_integrated/backend/src/models/setting.py",
    "gaara_ai_integrated/backend/src/models/user.py",
    "gaara_ai_integrated/backend/src/modules/config_2.py",
    "gaara_ai_integrated/backend/src/modules/config_3.py",
    "gaara_ai_integrated/backend/src/modules/config_8.py",
    "gaara_ai_integrated/backend/src/modules/constants.py",
    "gaara_ai_integrated/backend/src/modules/schemas_1.py",
    "gaara_ai_integrated/backend/src/modules/schemas_13.py",
    "gaara_ai_integrated/backend/src/modules/schemas_5.py",
    "gaara_ai_integrated/backend/src/modules/schemas_6.py",
    "gaara_ai_integrated/backend/static/__init__.py",
    "gaara_ai_integrated/backend/utils/__init__.py",
    "gaara_ai_integrated/backend/views/__init__.py"
  ]
}

### javascript_syntax ✅
الحالة: PASS
الرسالة: جميع ملفات JavaScript صحيحة: 78 ملف

### backend_dependencies ✅
الحالة: PASS
الرسالة: ملف requirements.txt موجود مع 131 تبعية
التفاصيل: {
  "dependencies": [
    "Flask==3.0.0",
    "Flask-SQLAlchemy==3.1.1",
    "Flask-CORS==4.0.0",
    "Flask-JWT-Extended==4.6.0",
    "Flask-RESTx==1.3.0",
    "Flask-Migrate==4.0.5",
    "Flask-Caching==2.1.0",
    "Flask-Mail==0.9.1",
    "Flask-Limiter==3.5.0",
    "SQLAlchemy==2.0.23",
    "Alembic==1.13.1",
    "psycopg2-binary==2.9.9",
    "pymongo==4.6.1",
    "bcrypt==4.1.2",
    "PyJWT==2.8.0",
    "cryptography==41.0.8",
    "passlib==1.7.4",
    "python-jose==3.3.0",
    "tensorflow==2.15.0",
    "tensorflow-hub==0.15.0",
    "scikit-learn==1.3.2",
    "numpy==1.24.4",
    "pandas==2.1.4",
    "opencv-python==4.8.1.78",
    "Pillow==10.1.0",
    "matplotlib==3.8.2",
    "seaborn==0.13.0",
    "torch==2.1.2",
    "torchvision==0.16.2",
    "transformers==4.36.2",
    "huggingface-hub==0.19.4",
    "opencv-contrib-python==4.8.1.78",
    "imageio==2.33.1",
    "scikit-image==0.22.0",
    "albumentations==1.3.1",
    "requests==2.31.0",
    "urllib3==2.1.0",
    "httpx==0.25.2",
    "aiohttp==3.9.1",
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "python-dotenv==1.0.0",
    "python-multipart==0.0.6",
    "email-validator==2.1.0",
    "validators==0.22.0",
    "pydantic==2.5.2",
    "marshmallow==3.20.2",
    "openpyxl==3.1.2",
    "xlsxwriter==3.1.9",
    "python-magic==0.4.27",
    "PyPDF2==3.0.1",
    "reportlab==4.0.8",
    "redis==5.0.1",
    "celery==5.3.4",
    "gunicorn==21.2.0",
    "gevent==23.9.1",
    "prometheus-flask-exporter==0.23.0",
    "structlog==23.2.0",
    "loguru==0.7.2",
    "pytest==7.4.3",
    "pytest-cov==4.1.0",
    "pytest-flask==1.3.0",
    "pytest-asyncio==0.21.1",
    "black==23.12.0",
    "flake8==6.1.0",
    "mypy==1.7.1",
    "isort==5.13.2",
    "pre-commit==3.6.0",
    "Werkzeug==3.0.1",
    "Jinja2==3.1.2",
    "MarkupSafe==2.1.3",
    "itsdangerous==2.1.2",
    "click==8.1.7",
    "blinker==1.7.0",
    "python-dateutil==2.8.2",
    "pytz==2023.3",
    "arrow==1.3.0",
    "tqdm==4.66.1",
    "colorama==0.4.6",
    "rich==13.7.0",
    "typer==0.9.0",
    "pyyaml==6.0.1",
    "boto3==1.34.0",
    "azure-storage-blob==12.19.0",
    "google-cloud-storage==2.10.0",
    "kombu==5.3.4",
    "billiard==4.2.0",
    "msgpack==1.0.7",
    "orjson==3.9.10",
    "websockets==12.0",
    "socketio==5.10.0",
    "python-socketio==5.10.0",
    "environs==11.0.0",
    "dynaconf==3.2.4",
    "healthcheck==1.3.3",
    "flasgger==0.9.7.1",
    "apispec==6.3.0",
    "rq==1.15.1",
    "schedule==1.2.1",
    "cerberus==1.3.5",
    "jsonschema==4.20.0",
    "babel==2.14.0",
    "flask-babel==4.0.0",
    "newrelic==9.4.0",
    "sentry-sdk==1.39.2",
    "flask-migrate==4.0.5",
    "flask-session==0.5.0",
    "slowapi==0.1.9",
    "schema==0.7.5",
    "asyncio==3.4.3",
    "aiofiles==23.2.1",
    "watchdog==3.0.0",
    "python-decouple==3.8",
    "oauthlib==3.2.2",
    "authlib==1.2.1",
    "zipfile36==0.1.3",
    "tarfile==0.1.0",
    "psutil==5.9.6",
    "py-cpuinfo==9.0.0",
    "nltk==3.8.1",
    "spacy==3.7.2",
    "geopy==2.4.1",
    "folium==0.15.1",
    "pandas-excel-writer==0.1.0",
    "csvkit==1.2.0",
    "pillow-simd==10.0.1.post1",
    "memory-profiler==0.61.0",
    "bandit==1.7.5",
    "safety==2.3.5",
    "sphinx==7.2.6",
    "sphinx-rtd-theme==2.0.0"
  ]
}

### frontend_dependencies ✅
الحالة: PASS
الرسالة: ملف package.json موجود مع 100 تبعية و 61 تبعية تطوير
التفاصيل: {
  "dependencies": [
    "react",
    "react-dom",
    "react-router-dom",
    "axios",
    "react-toastify",
    "recharts",
    "lucide-react",
    "@heroicons/react",
    "tailwindcss",
    "@tailwindcss/forms",
    "@tailwindcss/typography",
    "@tailwindcss/aspect-ratio",
    "clsx",
    "class-variance-authority",
    "tailwind-merge",
    "@radix-ui/react-dialog",
    "@radix-ui/react-dropdown-menu",
    "@radix-ui/react-label",
    "@radix-ui/react-select",
    "@radix-ui/react-separator",
    "@radix-ui/react-slot",
    "@radix-ui/react-switch",
    "@radix-ui/react-tabs",
    "@radix-ui/react-tooltip",
    "@radix-ui/react-progress",
    "@radix-ui/react-avatar",
    "@radix-ui/react-checkbox",
    "@radix-ui/react-accordion",
    "@radix-ui/react-alert-dialog",
    "@radix-ui/react-popover",
    "react-hook-form",
    "@hookform/resolvers",
    "zod",
    "date-fns",
    "react-day-picker",
    "framer-motion",
    "react-dropzone",
    "react-image-crop",
    "react-webcam",
    "chart.js",
    "react-chartjs-2",
    "html2canvas",
    "jspdf",
    "file-saver",
    "lodash",
    "moment",
    "@tanstack/react-query",
    "zustand",
    "immer",
    "react-beautiful-dnd",
    "react-virtualized",
    "react-window",
    "react-intersection-observer",
    "react-hotkeys-hook",
    "react-use",
    "ahooks",
    "react-error-boundary",
    "react-helmet-async",
    "react-loading-skeleton",
    "react-spinners",
    "react-transition-group",
    "react-spring",
    "react-gesture",
    "react-use-gesture",
    "react-hotjar",
    "react-gtm-module",
    "react-cookie",
    "js-cookie",
    "react-i18next",
    "i18next",
    "i18next-browser-languagedetector",
    "react-select",
    "react-datepicker",
    "react-color",
    "react-markdown",
    "remark-gfm",
    "react-syntax-highlighter",
    "react-pdf",
    "react-player",
    "react-qr-code",
    "qrcode.js",
    "react-barcode",
    "react-signature-canvas",
    "react-cropper",
    "cropperjs",
    "react-image-gallery",
    "react-lightbox-component",
    "react-photo-view",
    "react-zoom-pan-pinch",
    "react-map-gl",
    "mapbox-gl",
    "leaflet",
    "react-leaflet",
    "react-google-maps",
    "@googlemaps/react-wrapper",
    "socket.io-client",
    "workbox-window",
    "workbox-precaching",
    "workbox-routing",
    "workbox-strategies"
  ],
  "devDependencies": [
    "@vitejs/plugin-react",
    "@vitejs/plugin-react-swc",
    "vite",
    "vite-plugin-pwa",
    "vite-plugin-windicss",
    "vite-bundle-analyzer",
    "eslint",
    "eslint-plugin-react",
    "eslint-plugin-react-hooks",
    "eslint-plugin-react-refresh",
    "eslint-plugin-jsx-a11y",
    "eslint-plugin-import",
    "@typescript-eslint/eslint-plugin",
    "@typescript-eslint/parser",
    "typescript",
    "prettier",
    "prettier-plugin-tailwindcss",
    "autoprefixer",
    "postcss",
    "vitest",
    "jsdom",
    "@testing-library/react",
    "@testing-library/jest-dom",
    "@testing-library/user-event",
    "@vitest/ui",
    "@vitest/coverage-v8",
    "happy-dom",
    "@types/react",
    "@types/react-dom",
    "@types/lodash",
    "@types/file-saver",
    "@types/js-cookie",
    "@types/react-beautiful-dnd",
    "@types/react-virtualized",
    "@types/react-window",
    "@types/react-transition-group",
    "@types/react-color",
    "@types/react-syntax-highlighter",
    "@types/react-signature-canvas",
    "@types/leaflet",
    "msw",
    "storybook",
    "@storybook/react",
    "@storybook/react-vite",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-links",
    "@storybook/blocks",
    "@storybook/testing-library",
    "chromatic",
    "husky",
    "lint-staged",
    "commitizen",
    "cz-conventional-changelog",
    "@commitlint/cli",
    "@commitlint/config-conventional",
    "cross-env",
    "dotenv",
    "rimraf",
    "concurrently",
    "npm-run-all"
  ]
}

### docker_compose ✅
الحالة: PASS
الرسالة: ملف docker-compose.yml موجود مع 3 خدمة
التفاصيل: {
  "found_services": [
    "backend",
    "frontend",
    "database"
  ]
}

### backend_dockerfile ✅
الحالة: PASS
الرسالة: Dockerfile للواجهة الخلفية موجود

### frontend_dockerfile ✅
الحالة: PASS
الرسالة: Dockerfile للواجهة الأمامية موجود

### api_routes ✅
الحالة: PASS
الرسالة: تم العثور على 11 مسار API
التفاصيل: {
  "routes": [
    "/auth/profile",
    "/admin/users",
    "/diagnosis",
    "/statistics/dashboard",
    "/",
    "/plants",
    "/reports/farms",
    "/farms/<int:farm_id>",
    "/farms",
    "/auth/register",
    "/auth/login"
  ]
}

### frontend_components ✅
الحالة: PASS
الرسالة: تم العثور على 51 مكون و 17 صفحة
التفاصيل: {
  "components": [
    "components/Analytics/AdvancedAnalytics.jsx",
    "components/Charts/DashboardCharts.jsx",
    "components/Layout/Navbar.jsx",
    "components/Layout/Sidebar.jsx",
    "components/ui/accordion.jsx",
    "components/ui/alert-dialog.jsx",
    "components/ui/alert.jsx",
    "components/ui/aspect-ratio.jsx",
    "components/ui/avatar.jsx",
    "components/ui/badge.jsx",
    "components/ui/breadcrumb.jsx",
    "components/ui/button.jsx",
    "components/ui/calendar.jsx",
    "components/ui/card.jsx",
    "components/ui/carousel.jsx",
    "components/ui/chart.jsx",
    "components/ui/checkbox.jsx",
    "components/ui/collapsible.jsx",
    "components/ui/command.jsx",
    "components/ui/context-menu.jsx",
    "components/ui/dialog.jsx",
    "components/ui/drawer.jsx",
    "components/ui/dropdown-menu.jsx",
    "components/ui/form.jsx",
    "components/ui/hover-card.jsx",
    "components/ui/input-otp.jsx",
    "components/ui/input.jsx",
    "components/ui/label.jsx",
    "components/ui/menubar.jsx",
    "components/ui/navigation-menu.jsx",
    "components/ui/pagination.jsx",
    "components/ui/popover.jsx",
    "components/ui/progress.jsx",
    "components/ui/radio-group.jsx",
    "components/ui/resizable.jsx",
    "components/ui/scroll-area.jsx",
    "components/ui/select.jsx",
    "components/ui/separator.jsx",
    "components/ui/sheet.jsx",
    "components/ui/sidebar.jsx",
    "components/ui/skeleton.jsx",
    "components/ui/slider.jsx",
    "components/ui/sonner.jsx",
    "components/ui/switch.jsx",
    "components/ui/table.jsx",
    "components/ui/tabs.jsx",
    "components/ui/textarea.jsx",
    "components/ui/toggle-group.jsx",
    "components/ui/toggle.jsx",
    "components/ui/tooltip.jsx",
    "components/Router/AppRouter.jsx"
  ],
  "pages": [
    "pages/Analytics.jsx",
    "pages/Breeding.jsx",
    "pages/Companies.jsx",
    "pages/Crops.jsx",
    "pages/Dashboard.jsx",
    "pages/Diagnosis.jsx",
    "pages/Diseases.jsx",
    "pages/Farms.jsx",
    "pages/Login.jsx",
    "pages/Profile.jsx",
    "pages/Reports.jsx",
    "pages/Sensors.jsx",
    "pages/Settings.jsx",
    "pages/SetupWizard.jsx",
    "pages/Users.jsx",
    "pages/Dashboard/Dashboard.jsx",
    "pages/Dashboard/DashboardComplete.jsx"
  ]
}

### routing_configuration ✅
الحالة: PASS
الرسالة: تم العثور على 70 مسار في التوجيه
التفاصيل: {
  "routes": [
    "/search",
    "/diagnosis/history",
    "/crops/:id/edit",
    "/reports",
    "/analytics/diseases",
    "/admin/users",
    "/crops/:id",
    "/admin/roles",
    "/reports/farms",
    "/plants/create",
    "/dashboard",
    "/farms/:id",
    "/analytics/productivity",
    "/admin/roles/create",
    "/sensors/:id",
    "/server-error",
    "/register",
    "/admin/companies",
    "/admin/companies/:id",
    "/settings/profile",
    "/admin/companies/create",
    "/diagnosis",
    "/diagnosis/:id",
    "/admin/users/create",
    "/admin/backups",
    "/plants",
    "/analytics/farms/:id",
    "/admin/logs",
    "/notifications",
    "/forgot-password",
    "/contact",
    "*",
    "/diagnosis/create",
    "/unauthorized",
    "/analytics/plants/:id",
    "/reports/create",
    "/sensors",
    "/analytics",
    "/settings/change-password",
    "/diseases/:id",
    "/",
    "/diseases/:id/edit",
    "/admin/companies/:id/edit",
    "/help",
    "/sensors/create",
    "/reset-password/:token",
    "/plants/:id/edit",
    "/diseases/create",
    "/admin",
    "/admin/roles/:id",
    "/admin/settings",
    "/admin/users/:id/edit",
    "/reports/productivity",
    "/farms/:id/edit",
    "/admin/users/:id",
    "/settings/notifications",
    "/sensors/:id/edit",
    "/about",
    "/crops/create",
    "/admin/permissions",
    "/admin/roles/:id/edit",
    "/settings",
    "/login",
    "/reports/plants",
    "/plants/:id",
    "/crops",
    "/farms/create",
    "/farms",
    "/reports/:id",
    "/diseases"
  ]
}

### permissions_system ✅
الحالة: PASS
الرسالة: نظام الصلاحيات مكتمل مع 5 مكون
التفاصيل: {
  "components": [
    "PermissionType",
    "Module",
    "DefaultRole",
    "require_permission",
    "require_role"
  ]
}

### api_service_integration ✅
الحالة: PASS
الرسالة: خدمة API مكتملة مع 121 طريقة
التفاصيل: {
  "total_methods": 121,
  "auth_methods": 2,
  "crud_methods": 92,
  "methods": [
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "upload",
    "login",
    "register",
    "logout",
    "getProfile",
    "updateProfile",
    "changePassword",
    "forgotPassword",
    "resetPassword",
    "getFarms",
    "getFarm",
    "createFarm",
    "updateFarm",
    "deleteFarm",
    "getFarmStatistics"
  ]
}
