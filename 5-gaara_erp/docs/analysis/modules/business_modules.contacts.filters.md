# business_modules.contacts.filters

## Imports
- django_filters
- models

## Classes
- ContactFilter
  - attr: `name`
  - attr: `email`
  - attr: `phone`
  - attr: `city`
- Meta
  - attr: `model`
  - attr: `fields`

## Class Diagram

```mermaid
classDiagram
    class ContactFilter {
        +name
        +email
        +phone
        +city
    }
    class Meta {
        +model
        +fields
    }
    ContactFilter --> Meta
```
