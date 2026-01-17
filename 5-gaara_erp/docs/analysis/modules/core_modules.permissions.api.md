# core_modules.permissions.api

## Imports
- abc
- datetime
- django.conf
- django.contrib.auth
- django.utils
- exceptions
- forex_python.converter
- langfuse
- langfuse.model
- logging
- os
- time
- traceback
- typing

## Classes
- StatusChoices
  - attr: `PROCESSING`
  - attr: `COMPLETED`
  - attr: `FAILED`
- BaseAIAgent
  - method: `__init__`
  - method: `execute`
  - method: `_handle_execution_error`
  - method: `run`
- SalesDataAnalyzerAgent
  - method: `__init__`
  - method: `execute`
- ExchangeRateAgent
  - method: `__init__`
  - method: `execute`
- MockExchangeRateAgent
  - method: `__init__`
  - method: `execute`
- LocationDetectionAgent
  - method: `__init__`
  - method: `execute`
- AgentError
- AgentExecutionError
  - method: `__init__`
- AgentConfigurationError

## Functions
- log_system_error
- __init__
- execute
- _handle_execution_error
- run
- __init__
- execute
- __init__
- execute
- __init__
- execute
- __init__
- execute
- __init__

## Module Variables
- `logger`
- `User`

## Class Diagram

```mermaid
classDiagram
    class StatusChoices {
        +PROCESSING
        +COMPLETED
        +FAILED
    }
    class BaseAIAgent {
        +__init__()
        +execute()
        +_handle_execution_error()
        +run()
    }
    class SalesDataAnalyzerAgent {
        +__init__()
        +execute()
    }
    class ExchangeRateAgent {
        +__init__()
        +execute()
    }
    class MockExchangeRateAgent {
        +__init__()
        +execute()
    }
    class LocationDetectionAgent {
        +__init__()
        +execute()
    }
    class AgentError {
    }
    class AgentExecutionError {
        +__init__()
    }
    class AgentConfigurationError {
    }
```
