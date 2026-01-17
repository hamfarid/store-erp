# agricultural_modules.seed_hybridization.merged.serializers

## Imports
- models
- rest_framework

## Classes
- PlantVarietySerializer
- HybridVarietySerializer
  - attr: `parent_varieties`
- HybridizationSimulationSerializer
  - attr: `parent_varieties`
  - attr: `hybrid_varieties`
- HybridizationExperimentSerializer
  - attr: `parent_varieties`
- HybridizationProjectSerializer
  - attr: `team_members`
  - attr: `simulations`
  - attr: `experiments`
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
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class PlantVarietySerializer {
    }
    class HybridVarietySerializer {
        +parent_varieties
    }
    class HybridizationSimulationSerializer {
        +parent_varieties
        +hybrid_varieties
    }
    class HybridizationExperimentSerializer {
        +parent_varieties
    }
    class HybridizationProjectSerializer {
        +team_members
        +simulations
        +experiments
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
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    PlantVarietySerializer --> Meta
    PlantVarietySerializer --> Meta
    PlantVarietySerializer --> Meta
    PlantVarietySerializer --> Meta
    PlantVarietySerializer --> Meta
    HybridVarietySerializer --> Meta
    HybridVarietySerializer --> Meta
    HybridVarietySerializer --> Meta
    HybridVarietySerializer --> Meta
    HybridVarietySerializer --> Meta
    HybridizationSimulationSerializer --> Meta
    HybridizationSimulationSerializer --> Meta
    HybridizationSimulationSerializer --> Meta
    HybridizationSimulationSerializer --> Meta
    HybridizationSimulationSerializer --> Meta
    HybridizationExperimentSerializer --> Meta
    HybridizationExperimentSerializer --> Meta
    HybridizationExperimentSerializer --> Meta
    HybridizationExperimentSerializer --> Meta
    HybridizationExperimentSerializer --> Meta
    HybridizationProjectSerializer --> Meta
    HybridizationProjectSerializer --> Meta
    HybridizationProjectSerializer --> Meta
    HybridizationProjectSerializer --> Meta
    HybridizationProjectSerializer --> Meta
```
