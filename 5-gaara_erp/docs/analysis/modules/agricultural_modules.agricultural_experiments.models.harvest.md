# agricultural_modules.agricultural_experiments.models.harvest

## Imports
- django.contrib.auth
- django.core.validators
- django.db
- django.utils.translation
- experiment

## Classes
- Harvest
  - attr: `experiment_variety`
  - attr: `harvest_number`
  - attr: `harvest_date`
  - attr: `fruit_count`
  - attr: `fruit_weight`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - attr: `created_by`
  - method: `__str__`
  - method: `average_fruit_weight`
- HarvestQualityGrade
  - attr: `QUALITY_GRADE_CHOICES`
  - attr: `harvest`
  - attr: `grade`
  - attr: `fruit_count`
  - attr: `fruit_weight`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- FruitSpecification
  - attr: `experiment_variety`
  - attr: `evaluation_date`
  - attr: `length_cm`
  - attr: `shape_uniformity_rating`
  - attr: `fruit_deformity_rate`
  - attr: `firmness_rating`
  - attr: `color_description`
  - attr: `color_rating`
  - attr: `storage_transport_tolerance_rating`
  - attr: `brix_value`
  - attr: `notes`
  - attr: `created_at`
  - method: `__str__`
- PlantSpecification
  - attr: `experiment_variety`
  - attr: `evaluation_date`
  - attr: `earliness_rating`
  - attr: `plant_vigor_rating`
  - attr: `leaf_shape_description`
  - attr: `fruit_coverage_rating`
  - attr: `fungal_resistance_rating`
  - attr: `bacterial_resistance_rating`
  - attr: `insect_resistance_rating`
  - attr: `viral_resistance_rating`
  - attr: `cold_tolerance_rating`
  - attr: `heat_tolerance_rating`
  - attr: `soil_salinity_tolerance_rating`
  - attr: `water_salinity_tolerance_rating`
  - attr: `drought_tolerance_rating`
  - attr: `notes`
  - attr: `created_at`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
  - attr: `unique_together`
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
- average_fruit_weight
- __str__
- __str__
- __str__

## Module Variables
- `User`
- `RATING_CHOICES`

## Class Diagram

```mermaid
classDiagram
    class Harvest {
        +experiment_variety
        +harvest_number
        +harvest_date
        +fruit_count
        +fruit_weight
        +... (4 more)
        +__str__()
        +average_fruit_weight()
    }
    class HarvestQualityGrade {
        +QUALITY_GRADE_CHOICES
        +harvest
        +grade
        +fruit_count
        +fruit_weight
        +... (2 more)
        +__str__()
    }
    class FruitSpecification {
        +experiment_variety
        +evaluation_date
        +length_cm
        +shape_uniformity_rating
        +fruit_deformity_rate
        +... (7 more)
        +__str__()
    }
    class PlantSpecification {
        +experiment_variety
        +evaluation_date
        +earliness_rating
        +plant_vigor_rating
        +leaf_shape_description
        +... (12 more)
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
        +unique_together
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
    Harvest --> Meta
    Harvest --> Meta
    Harvest --> Meta
    Harvest --> Meta
    HarvestQualityGrade --> Meta
    HarvestQualityGrade --> Meta
    HarvestQualityGrade --> Meta
    HarvestQualityGrade --> Meta
    FruitSpecification --> Meta
    FruitSpecification --> Meta
    FruitSpecification --> Meta
    FruitSpecification --> Meta
    PlantSpecification --> Meta
    PlantSpecification --> Meta
    PlantSpecification --> Meta
    PlantSpecification --> Meta
```
