"""API metadata decorator & lightweight schema registry.

Provides:
        @api_meta(summary="...", description="...", tags=[...],
                            responses={...}, request_schema=...,
                            response_schema=...)

Schemas are simple JSON-serializable dict definitions (OpenAPI fragments).
Avoids external deps (e.g., pydantic) while still enabling enrichment.
"""

from __future__ import annotations
from functools import wraps
from typing import Any, Callable, Dict, Optional, List

# Global registries; OpenAPI generator will introspect.

SCHEMA_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_schema(name: str, schema: Dict[str, Any]) -> None:
    """Register a schema by name (idempotent)."""
    if name not in SCHEMA_REGISTRY:
        SCHEMA_REGISTRY[name] = schema


def api_meta(
    summary: str,
    description: str | None = None,
    tags: Optional[List[str]] = None,
    responses: Optional[Dict[str, Dict[str, Any]]] = None,
    request_schema: str | None = None,
    response_schema: str | None = None,
):
    """Decorator to annotate Flask view functions with OpenAPI metadata.

    Parameters
    ----------
    summary: short endpoint summary
    description: longer description (markdown allowed)
    tags: list of grouping tags
    responses: mapping of status -> response object (OpenAPI fragment)
    request_schema: registered schema name for requestBody (application/json)
    response_schema: registered schema name for 200 response body
    """

    def decorator(func: Callable):
        meta = {
            "summary": summary,
            "description": description,
            "tags": tags,
            "responses": responses,
            "request_schema": request_schema,
            "response_schema": response_schema,
        }
        setattr(func, "_api_meta", meta)

        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore[misc]
            return func(*args, **kwargs)

        return wrapper

    return decorator
