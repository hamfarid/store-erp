# services_modules.beneficiaries.serializers

## Imports
- django.contrib.auth.models
- django.db
- models
- rest_framework

## Classes
- UserSerializer
- BeneficiaryCategorySerializer
- BeneficiaryStatusSerializer
- BeneficiarySerializer
  - attr: `category`
  - attr: `category_id`
  - attr: `status`
  - attr: `status_id`
  - attr: `case_manager`
  - attr: `case_manager_id`
  - attr: `registered_by`
  - attr: `registered_by_id`
- BeneficiaryDocumentSerializer
  - attr: `beneficiary`
  - attr: `beneficiary_id`
  - attr: `uploaded_by`
  - attr: `uploaded_by_id`
- BeneficiaryContactSerializer
  - attr: `beneficiary`
  - attr: `beneficiary_id`
  - attr: `added_by`
  - attr: `added_by_id`
- BeneficiaryServiceSerializer
  - attr: `beneficiary`
  - attr: `beneficiary_id`
  - attr: `provided_by`
  - attr: `provided_by_id`
  - attr: `recorded_by`
  - attr: `recorded_by_id`
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
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Class Diagram

```mermaid
classDiagram
    class UserSerializer {
    }
    class BeneficiaryCategorySerializer {
    }
    class BeneficiaryStatusSerializer {
    }
    class BeneficiarySerializer {
        +category
        +category_id
        +status
        +status_id
        +case_manager
        +... (3 more)
    }
    class BeneficiaryDocumentSerializer {
        +beneficiary
        +beneficiary_id
        +uploaded_by
        +uploaded_by_id
    }
    class BeneficiaryContactSerializer {
        +beneficiary
        +beneficiary_id
        +added_by
        +added_by_id
    }
    class BeneficiaryServiceSerializer {
        +beneficiary
        +beneficiary_id
        +provided_by
        +provided_by_id
        +recorded_by
        +... (1 more)
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
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    UserSerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryCategorySerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiaryStatusSerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiarySerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryDocumentSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryContactSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
    BeneficiaryServiceSerializer --> Meta
```
