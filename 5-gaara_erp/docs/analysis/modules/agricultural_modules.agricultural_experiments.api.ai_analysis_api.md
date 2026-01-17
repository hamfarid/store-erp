# agricultural_modules.agricultural_experiments.api.ai_analysis_api

## Imports
- models.ai_analysis
- rest_framework
- rest_framework.decorators
- rest_framework.permissions
- rest_framework.response
- services.ai_analysis_service

## Classes
- VarietyAIAnalysisSerializer
  - attr: `variety_name`
  - method: `get_variety_name`
- AIAnalysisSerializer
  - attr: `analysis_type_display`
  - attr: `variety_analyses`
- AIAnalysisViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - method: `get_queryset`
  - method: `analyze_variety_performance`
  - method: `compare_varieties`
  - method: `predict_variety_performance`
  - method: `analyze_trial_performance`
- VarietyAIAnalysisViewSet
  - attr: `queryset`
  - attr: `serializer_class`
  - attr: `permission_classes`
  - method: `get_queryset`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Functions
- get_variety_name
- get_queryset
- analyze_variety_performance
- compare_varieties
- predict_variety_performance
- analyze_trial_performance
- get_queryset

## Class Diagram

```mermaid
classDiagram
    class VarietyAIAnalysisSerializer {
        +variety_name
        +get_variety_name()
    }
    class AIAnalysisSerializer {
        +analysis_type_display
        +variety_analyses
    }
    class AIAnalysisViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +get_queryset()
        +analyze_variety_performance()
        +compare_varieties()
        +predict_variety_performance()
        +analyze_trial_performance()
    }
    class VarietyAIAnalysisViewSet {
        +queryset
        +serializer_class
        +permission_classes
        +get_queryset()
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
    VarietyAIAnalysisSerializer --> Meta
    VarietyAIAnalysisSerializer --> Meta
    AIAnalysisSerializer --> Meta
    AIAnalysisSerializer --> Meta
    AIAnalysisViewSet --> Meta
    AIAnalysisViewSet --> Meta
    VarietyAIAnalysisViewSet --> Meta
    VarietyAIAnalysisViewSet --> Meta
```
