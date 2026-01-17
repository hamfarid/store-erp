# agricultural_modules.seed_production.serializers

## Imports
- django.utils.translation
- models
- rest_framework

## Classes
- SeedProductionOrderSerializer
- SeedProductionOrderCreateSerializer
- SeedProductionOrderUpdateSerializer
- InventoryVerificationSerializer
- CreateLotFromOrderSerializer
  - attr: `lot_number`
  - attr: `expected_seed_quantity_kg`
- SeedProductionLotSerializer
- SeedProductionLotDetailSerializer
- SeedProductionLotCreateSerializer
- SeedProductionLotUpdateSerializer
- PlantingRecordSerializer
  - attr: `actual_planting_date`
  - attr: `notes`
- HarvestRecordSerializer
  - attr: `actual_harvest_date`
  - attr: `harvested_quantity_kg`
  - attr: `notes`
- SeedProductionPlanSerializer
- SeedProductionPlanCreateSerializer
- SeedProductionPlanUpdateSerializer
- SeedLotTestSerializer
- SeedLotTestCreateSerializer
- SeedLotTestUpdateSerializer
- GerminationTestSerializer
  - attr: `germination_rate_percent`
  - attr: `test_date`
  - attr: `notes`
- PurityTestSerializer
  - attr: `purity_percent`
  - attr: `test_date`
  - attr: `notes`
- SeedTreatmentLogSerializer
- SeedTreatmentLogCreateSerializer
- SeedPackagingSerializer
- SeedPackagingCreateSerializer
- CompletePackagingSerializer
  - attr: `actual_packaging_date`
  - attr: `actual_quantity_kg`
  - attr: `notes`
- LotChangeLogSerializer
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `exclude`
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
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`

## Class Diagram

```mermaid
classDiagram
    class SeedProductionOrderSerializer {
    }
    class SeedProductionOrderCreateSerializer {
    }
    class SeedProductionOrderUpdateSerializer {
    }
    class InventoryVerificationSerializer {
    }
    class CreateLotFromOrderSerializer {
        +lot_number
        +expected_seed_quantity_kg
    }
    class SeedProductionLotSerializer {
    }
    class SeedProductionLotDetailSerializer {
    }
    class SeedProductionLotCreateSerializer {
    }
    class SeedProductionLotUpdateSerializer {
    }
    class PlantingRecordSerializer {
        +actual_planting_date
        +notes
    }
    class HarvestRecordSerializer {
        +actual_harvest_date
        +harvested_quantity_kg
        +notes
    }
    class SeedProductionPlanSerializer {
    }
    class SeedProductionPlanCreateSerializer {
    }
    class SeedProductionPlanUpdateSerializer {
    }
    class SeedLotTestSerializer {
    }
    class SeedLotTestCreateSerializer {
    }
    class SeedLotTestUpdateSerializer {
    }
    class GerminationTestSerializer {
        +germination_rate_percent
        +test_date
        +notes
    }
    class PurityTestSerializer {
        +purity_percent
        +test_date
        +notes
    }
    class SeedTreatmentLogSerializer {
    }
    class SeedTreatmentLogCreateSerializer {
    }
    class SeedPackagingSerializer {
    }
    class SeedPackagingCreateSerializer {
    }
    class CompletePackagingSerializer {
        +actual_packaging_date
        +actual_quantity_kg
        +notes
    }
    class LotChangeLogSerializer {
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +exclude
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
        +exclude
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderCreateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    SeedProductionOrderUpdateSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    InventoryVerificationSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    CreateLotFromOrderSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotDetailSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotCreateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    SeedProductionLotUpdateSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    PlantingRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    HarvestRecordSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanCreateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedProductionPlanUpdateSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestCreateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    SeedLotTestUpdateSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    GerminationTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    PurityTestSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedTreatmentLogCreateSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    SeedPackagingCreateSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    CompletePackagingSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
    LotChangeLogSerializer --> Meta
```
