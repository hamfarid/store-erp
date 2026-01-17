# business_modules.contacts.serializers

## Imports
- admin_modules.communication.models
- models
- rest_framework

## Classes
- ContactCategorySerializer
- ContactTagSerializer
- ContactSerializer
  - attr: `category_name`
  - attr: `contact_type_display`
  - attr: `tags_names`
  - method: `to_representation`
- CommunicationLogSerializer
  - attr: `contact_name`
  - attr: `communication_type_display`
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
- to_representation

## Class Diagram

```mermaid
classDiagram
    class ContactCategorySerializer {
    }
    class ContactTagSerializer {
    }
    class ContactSerializer {
        +category_name
        +contact_type_display
        +tags_names
        +to_representation()
    }
    class CommunicationLogSerializer {
        +contact_name
        +communication_type_display
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
    ContactCategorySerializer --> Meta
    ContactCategorySerializer --> Meta
    ContactCategorySerializer --> Meta
    ContactCategorySerializer --> Meta
    ContactTagSerializer --> Meta
    ContactTagSerializer --> Meta
    ContactTagSerializer --> Meta
    ContactTagSerializer --> Meta
    ContactSerializer --> Meta
    ContactSerializer --> Meta
    ContactSerializer --> Meta
    ContactSerializer --> Meta
    CommunicationLogSerializer --> Meta
    CommunicationLogSerializer --> Meta
    CommunicationLogSerializer --> Meta
    CommunicationLogSerializer --> Meta
```
