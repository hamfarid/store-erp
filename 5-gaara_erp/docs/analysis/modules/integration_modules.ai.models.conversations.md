# integration_modules.ai.models.conversations

## Imports
- django.conf
- django.db
- django.utils
- django.utils.translation

## Classes
- Conversation
  - attr: `user`
  - attr: `title`
  - attr: `start_time`
  - attr: `last_updated`
  - attr: `summary`
  - method: `__str__`
- Message
  - attr: `conversation`
  - attr: `sender_type`
  - attr: `text_content`
  - attr: `timestamp`
  - attr: `feedback_score`
  - attr: `feedback_notes`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `ordering`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `indexes`
- Sender
  - attr: `USER`
  - attr: `AI`
- Meta
  - attr: `app_label`
  - attr: `ordering`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `indexes`

## Functions
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class Conversation {
        +user
        +title
        +start_time
        +last_updated
        +summary
        +__str__()
    }
    class Message {
        +conversation
        +sender_type
        +text_content
        +timestamp
        +feedback_score
        +... (1 more)
        +__str__()
    }
    class Meta {
        +app_label
        +ordering
        +verbose_name
        +verbose_name_plural
        +indexes
    }
    class Sender {
        +USER
        +AI
    }
    class Meta {
        +app_label
        +ordering
        +verbose_name
        +verbose_name_plural
        +indexes
    }
    Conversation --> Meta
    Conversation --> Meta
    Message --> Meta
    Message --> Meta
    Sender --> Meta
    Sender --> Meta
```
