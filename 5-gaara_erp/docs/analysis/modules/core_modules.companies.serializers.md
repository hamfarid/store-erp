# core_modules.companies.serializers

## Imports
- models
- rest_framework

## Classes
- CountrySerializer
- RegionSerializer
- CompanySerializer
  - attr: `country_name`
  - attr: `branches_count`
  - method: `get_branches_count`
- BranchSerializer
  - attr: `company_name`
- CompanyListSerializer
  - attr: `branches_count`
  - method: `get_branches_count`
- BranchListSerializer
  - attr: `company_name`
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

## Functions
- get_branches_count
- get_branches_count

## Class Diagram

```mermaid
classDiagram
    class CountrySerializer {
    }
    class RegionSerializer {
    }
    class CompanySerializer {
        +country_name
        +branches_count
        +get_branches_count()
    }
    class BranchSerializer {
        +company_name
    }
    class CompanyListSerializer {
        +branches_count
        +get_branches_count()
    }
    class BranchListSerializer {
        +company_name
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
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    CountrySerializer --> Meta
    RegionSerializer --> Meta
    RegionSerializer --> Meta
    RegionSerializer --> Meta
    RegionSerializer --> Meta
    RegionSerializer --> Meta
    RegionSerializer --> Meta
    CompanySerializer --> Meta
    CompanySerializer --> Meta
    CompanySerializer --> Meta
    CompanySerializer --> Meta
    CompanySerializer --> Meta
    CompanySerializer --> Meta
    BranchSerializer --> Meta
    BranchSerializer --> Meta
    BranchSerializer --> Meta
    BranchSerializer --> Meta
    BranchSerializer --> Meta
    BranchSerializer --> Meta
    CompanyListSerializer --> Meta
    CompanyListSerializer --> Meta
    CompanyListSerializer --> Meta
    CompanyListSerializer --> Meta
    CompanyListSerializer --> Meta
    CompanyListSerializer --> Meta
    BranchListSerializer --> Meta
    BranchListSerializer --> Meta
    BranchListSerializer --> Meta
    BranchListSerializer --> Meta
    BranchListSerializer --> Meta
    BranchListSerializer --> Meta
```
