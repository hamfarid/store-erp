# utility_modules.locale.serializers

## Imports
- django.utils.translation
- models
- rest_framework

## Classes
- LanguageSerializer
  - method: `validate`
- LanguageListSerializer
  - attr: `name_localized`
  - method: `get_name_localized`
- TranslationKeySerializer
- TranslationSerializer
  - attr: `key_name`
  - attr: `language_code`
  - method: `validate`
- TranslationDetailSerializer
  - attr: `key`
  - attr: `language`
- TranslationBulkCreateSerializer
  - attr: `key_id`
  - attr: `translations`
  - method: `validate`
- UserLanguagePreferenceSerializer
  - attr: `language_code`
  - attr: `language_name`
- SetUserLanguageSerializer
  - attr: `language_code`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
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
- validate
- get_name_localized
- validate
- validate

## Class Diagram

```mermaid
classDiagram
    class LanguageSerializer {
        +validate()
    }
    class LanguageListSerializer {
        +name_localized
        +get_name_localized()
    }
    class TranslationKeySerializer {
    }
    class TranslationSerializer {
        +key_name
        +language_code
        +validate()
    }
    class TranslationDetailSerializer {
        +key
        +language
    }
    class TranslationBulkCreateSerializer {
        +key_id
        +translations
        +validate()
    }
    class UserLanguagePreferenceSerializer {
        +language_code
        +language_name
    }
    class SetUserLanguageSerializer {
        +language_code
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
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
    LanguageSerializer --> Meta
    LanguageSerializer --> Meta
    LanguageSerializer --> Meta
    LanguageSerializer --> Meta
    LanguageSerializer --> Meta
    LanguageSerializer --> Meta
    LanguageListSerializer --> Meta
    LanguageListSerializer --> Meta
    LanguageListSerializer --> Meta
    LanguageListSerializer --> Meta
    LanguageListSerializer --> Meta
    LanguageListSerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationKeySerializer --> Meta
    TranslationSerializer --> Meta
    TranslationSerializer --> Meta
    TranslationSerializer --> Meta
    TranslationSerializer --> Meta
    TranslationSerializer --> Meta
    TranslationSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationDetailSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    TranslationBulkCreateSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    UserLanguagePreferenceSerializer --> Meta
    SetUserLanguageSerializer --> Meta
    SetUserLanguageSerializer --> Meta
    SetUserLanguageSerializer --> Meta
    SetUserLanguageSerializer --> Meta
    SetUserLanguageSerializer --> Meta
    SetUserLanguageSerializer --> Meta
```
