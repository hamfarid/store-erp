# core_modules.rag.serializers

## Imports
- __future__
- core_modules.rag.models
- django.contrib.auth
- rest_framework

## Classes
- DocumentSerializer
- ChunkSerializer
  - attr: `document_title`
- MemorySerializer
  - attr: `user_username`
- IngestRequestSerializer
  - attr: `title`
  - attr: `text`
  - attr: `source`
  - attr: `metadata`
- SearchRequestSerializer
  - attr: `query`
  - attr: `top_k`
  - attr: `threshold`
- SearchResultSerializer
  - attr: `chunk_id`
  - attr: `document_id`
  - attr: `document_title`
  - attr: `text`
  - attr: `score`
  - attr: `chunk_index`
- SearchResponseSerializer
  - attr: `query`
  - attr: `results`
  - attr: `total_results`
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

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class DocumentSerializer {
    }
    class ChunkSerializer {
        +document_title
    }
    class MemorySerializer {
        +user_username
    }
    class IngestRequestSerializer {
        +title
        +text
        +source
        +metadata
    }
    class SearchRequestSerializer {
        +query
        +top_k
        +threshold
    }
    class SearchResultSerializer {
        +chunk_id
        +document_id
        +document_title
        +text
        +score
        +... (1 more)
    }
    class SearchResponseSerializer {
        +query
        +results
        +total_results
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
    DocumentSerializer --> Meta
    DocumentSerializer --> Meta
    DocumentSerializer --> Meta
    ChunkSerializer --> Meta
    ChunkSerializer --> Meta
    ChunkSerializer --> Meta
    MemorySerializer --> Meta
    MemorySerializer --> Meta
    MemorySerializer --> Meta
    IngestRequestSerializer --> Meta
    IngestRequestSerializer --> Meta
    IngestRequestSerializer --> Meta
    SearchRequestSerializer --> Meta
    SearchRequestSerializer --> Meta
    SearchRequestSerializer --> Meta
    SearchResultSerializer --> Meta
    SearchResultSerializer --> Meta
    SearchResultSerializer --> Meta
    SearchResponseSerializer --> Meta
    SearchResponseSerializer --> Meta
    SearchResponseSerializer --> Meta
```
