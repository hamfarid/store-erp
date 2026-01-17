#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Metadata and Schema Registration System
Provides centralized API metadata management and schema registration
"""

import logging
from typing import Dict, Any, Optional, List
from functools import wraps

logger = logging.getLogger(__name__)

# Global API metadata storage
_api_metadata: Dict[str, Dict[str, Any]] = {}
_registered_schemas: Dict[str, Any] = {}


class APIMetadata:
    """
    Centralized API metadata management
    """

    def __init__(self):
        self.metadata = _api_metadata
        self.schemas = _registered_schemas

    def register_endpoint(
        self,
        endpoint: str,
        method: str,
        description: str,
        request_schema: Optional[str] = None,
        response_schema: Optional[str] = None,
        auth_required: bool = True,
        rate_limit: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Register API endpoint metadata

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            description: Endpoint description
            request_schema: Request schema name
            response_schema: Response schema name
            auth_required: Whether authentication is required
            rate_limit: Rate limit specification
            tags: Endpoint tags for categorization
        """
        key = f"{method}:{endpoint}"
        self.metadata[key] = {
            "endpoint": endpoint,
            "method": method,
            "description": description,
            "request_schema": request_schema,
            "response_schema": response_schema,
            "auth_required": auth_required,
            "rate_limit": rate_limit,
            "tags": tags or [],
        }
        logger.debug(f"Registered API endpoint: {key}")

    def get_endpoint_meta(self, endpoint: str, method: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific endpoint"""
        key = f"{method}:{endpoint}"
        return self.metadata.get(key)

    def get_all_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered endpoints"""
        return self.metadata.copy()

    def register_schema(self, name: str, schema: Any):
        """
        Register a validation schema

        Args:
            name: Schema name
            schema: Schema object (Marshmallow, Pydantic, etc.)
        """
        self.schemas[name] = schema
        logger.debug(f"Registered schema: {name}")

    def get_schema(self, name: str) -> Optional[Any]:
        """Get a registered schema by name"""
        return self.schemas.get(name)


# Global instance
api_meta = APIMetadata()


def register_schema(name: str, schema: Any):
    """
    Convenience function to register a schema

    Args:
        name: Schema name
        schema: Schema object
    """
    api_meta.register_schema(name, schema)


def api_endpoint(
    description: Optional[str] = None,
    summary: Optional[str] = None,
    request_schema: Optional[str] = None,
    response_schema: Optional[str] = None,
    auth_required: bool = True,
    rate_limit: Optional[str] = None,
    tags: Optional[List[str]] = None,
):
    """
    Decorator to register API endpoint metadata

    Usage:
        @api_endpoint(
            description="User login",
            request_schema="LoginSchema",
            response_schema="TokenSchema",
            tags=["auth"]
        )
        @auth_bp.route('/login', methods=['POST'])
        def login():
            ...
    """
    # Use summary as description if description is not provided
    if not description and summary:
        description = summary

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store metadata on the function
        wrapper._api_meta = {
            "description": description,
            "request_schema": request_schema,
            "response_schema": response_schema,
            "auth_required": auth_required,
            "rate_limit": rate_limit,
            "tags": tags or [],
        }

        return wrapper

    return decorator


# Export all
__all__ = ["api_meta", "register_schema", "api_endpoint", "APIMetadata"]
