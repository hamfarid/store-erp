#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2.61: Advanced Search with Filters

Generic search functionality with filtering, sorting, and pagination.
"""

import logging
from typing import List, Dict, Any, Optional, Type, Tuple
from dataclasses import dataclass, field
from enum import Enum
from sqlalchemy import or_, and_, func, desc, asc
from sqlalchemy.orm import Query
from flask import request

logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Data Classes
# =============================================================================


class FilterOperator(Enum):
    """Available filter operators."""

    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IN = "in"
    NOT_IN = "not_in"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    BETWEEN = "between"


@dataclass
class SearchFilter:
    """A single search filter."""

    field: str
    operator: FilterOperator
    value: Any


@dataclass
class SortConfig:
    """Sort configuration."""

    field: str
    direction: str = "asc"  # 'asc' or 'desc'


@dataclass
class SearchParams:
    """Complete search parameters."""

    query: Optional[str] = None
    filters: List[SearchFilter] = field(default_factory=list)
    sort: List[SortConfig] = field(default_factory=list)
    page: int = 1
    page_size: int = 20
    search_fields: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Search result with pagination metadata."""

    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "page_size": self.page_size,
                "total_pages": self.total_pages,
                "has_next": self.has_next,
                "has_prev": self.has_prev,
            },
        }


# =============================================================================
# Search Service
# =============================================================================


class SearchService:
    """
    P2.61: Generic search service for SQLAlchemy models.

    Provides:
    - Full-text search across multiple fields
    - Dynamic filtering with multiple operators
    - Multi-column sorting
    - Pagination
    """

    @staticmethod
    def apply_filter(query: Query, model: Type, filter_config: SearchFilter) -> Query:
        """Apply a single filter to the query."""
        if not hasattr(model, filter_config.field):
            logger.warning(f"Model {model.__name__} has no field {filter_config.field}")
            return query

        column = getattr(model, filter_config.field)
        value = filter_config.value
        op = filter_config.operator

        if op == FilterOperator.EQUALS:
            return query.filter(column == value)
        elif op == FilterOperator.NOT_EQUALS:
            return query.filter(column != value)
        elif op == FilterOperator.GREATER_THAN:
            return query.filter(column > value)
        elif op == FilterOperator.GREATER_THAN_OR_EQUAL:
            return query.filter(column >= value)
        elif op == FilterOperator.LESS_THAN:
            return query.filter(column < value)
        elif op == FilterOperator.LESS_THAN_OR_EQUAL:
            return query.filter(column <= value)
        elif op == FilterOperator.CONTAINS:
            return query.filter(column.ilike(f"%{value}%"))
        elif op == FilterOperator.STARTS_WITH:
            return query.filter(column.ilike(f"{value}%"))
        elif op == FilterOperator.ENDS_WITH:
            return query.filter(column.ilike(f"%{value}"))
        elif op == FilterOperator.IN:
            return query.filter(
                column.in_(value if isinstance(value, list) else [value])
            )
        elif op == FilterOperator.NOT_IN:
            return query.filter(
                ~column.in_(value if isinstance(value, list) else [value])
            )
        elif op == FilterOperator.IS_NULL:
            return query.filter(column.is_(None))
        elif op == FilterOperator.IS_NOT_NULL:
            return query.filter(column.isnot(None))
        elif op == FilterOperator.BETWEEN:
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return query.filter(column.between(value[0], value[1]))

        return query

    @staticmethod
    def apply_text_search(
        query: Query, model: Type, search_text: str, search_fields: List[str]
    ) -> Query:
        """Apply full-text search across multiple fields."""
        if not search_text or not search_fields:
            return query

        conditions = []
        for field_name in search_fields:
            if hasattr(model, field_name):
                column = getattr(model, field_name)
                conditions.append(column.ilike(f"%{search_text}%"))

        if conditions:
            return query.filter(or_(*conditions))

        return query

    @staticmethod
    def apply_sorting(
        query: Query, model: Type, sort_configs: List[SortConfig]
    ) -> Query:
        """Apply sorting to the query."""
        for sort in sort_configs:
            if hasattr(model, sort.field):
                column = getattr(model, sort.field)
                if sort.direction.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))

        return query

    @staticmethod
    def search(
        model: Type, params: SearchParams, base_query: Query = None
    ) -> SearchResult:
        """
        Execute a search with filters, sorting, and pagination.

        Args:
            model: SQLAlchemy model class
            params: Search parameters
            base_query: Optional base query to start with

        Returns:
            SearchResult with items and pagination metadata
        """
        # Start with base query or model query
        query = base_query if base_query is not None else model.query

        # Apply text search
        if params.query and params.search_fields:
            query = SearchService.apply_text_search(
                query, model, params.query, params.search_fields
            )

        # Apply filters
        for filter_config in params.filters:
            query = SearchService.apply_filter(query, model, filter_config)

        # Get total count before pagination
        total = query.count()

        # Apply sorting
        if params.sort:
            query = SearchService.apply_sorting(query, model, params.sort)

        # Calculate pagination
        total_pages = (
            (total + params.page_size - 1) // params.page_size
            if params.page_size > 0
            else 1
        )
        offset = (params.page - 1) * params.page_size

        # Apply pagination
        items = query.offset(offset).limit(params.page_size).all()

        return SearchResult(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1,
        )


# =============================================================================
# Request Parser
# =============================================================================


class SearchRequestParser:
    """
    P2.61: Parse search parameters from HTTP request.

    Supports query string format:
    - q: Search query text
    - page: Page number
    - page_size: Items per page
    - sort: Comma-separated fields (prefix with - for desc)
    - filter[field][operator]: Filter value

    Examples:
        ?q=laptop&page=1&page_size=20&sort=-created_at,name
        ?filter[price][gte]=100&filter[price][lte]=500
        ?filter[category_id][in]=1,2,3
    """

    OPERATOR_MAP = {
        "eq": FilterOperator.EQUALS,
        "ne": FilterOperator.NOT_EQUALS,
        "gt": FilterOperator.GREATER_THAN,
        "gte": FilterOperator.GREATER_THAN_OR_EQUAL,
        "lt": FilterOperator.LESS_THAN,
        "lte": FilterOperator.LESS_THAN_OR_EQUAL,
        "contains": FilterOperator.CONTAINS,
        "starts_with": FilterOperator.STARTS_WITH,
        "ends_with": FilterOperator.ENDS_WITH,
        "in": FilterOperator.IN,
        "not_in": FilterOperator.NOT_IN,
        "is_null": FilterOperator.IS_NULL,
        "is_not_null": FilterOperator.IS_NOT_NULL,
        "between": FilterOperator.BETWEEN,
    }

    @classmethod
    def parse(
        cls,
        search_fields: List[str] = None,
        default_page_size: int = 20,
        max_page_size: int = 100,
    ) -> SearchParams:
        """Parse search parameters from current Flask request."""
        # Get query text
        query_text = request.args.get("q", "")

        # Get pagination
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", default_page_size, type=int)
        page_size = min(page_size, max_page_size)

        # Parse sort
        sort_configs = []
        sort_param = request.args.get("sort", "")
        if sort_param:
            for sort_field in sort_param.split(","):
                sort_field = sort_field.strip()
                if sort_field.startswith("-"):
                    sort_configs.append(
                        SortConfig(field=sort_field[1:], direction="desc")
                    )
                else:
                    sort_configs.append(SortConfig(field=sort_field, direction="asc"))

        # Parse filters
        filters = []
        for key, value in request.args.items():
            if key.startswith("filter[") and "]" in key:
                # Parse filter[field][operator] format
                parts = (
                    key.replace("filter[", "").replace("]", "[").rstrip("[").split("[")
                )
                if len(parts) >= 1:
                    field_name = parts[0]
                    operator_name = parts[1] if len(parts) > 1 else "eq"
                    operator = cls.OPERATOR_MAP.get(
                        operator_name, FilterOperator.EQUALS
                    )

                    # Handle list values for IN operator
                    if operator in (FilterOperator.IN, FilterOperator.NOT_IN):
                        value = [v.strip() for v in value.split(",")]
                    # Handle between operator
                    elif operator == FilterOperator.BETWEEN:
                        value = [v.strip() for v in value.split(",")]

                    filters.append(
                        SearchFilter(field=field_name, operator=operator, value=value)
                    )

        return SearchParams(
            query=query_text,
            filters=filters,
            sort=sort_configs,
            page=page,
            page_size=page_size,
            search_fields=search_fields or [],
        )


# =============================================================================
# Search Decorator
# =============================================================================


def searchable(
    model: Type,
    search_fields: List[str],
    default_sort: str = None,
    max_page_size: int = 100,
):
    """
    Decorator to add search functionality to a Flask route.

    Usage:
        @app.route('/products')
        @searchable(Product, ['name', 'sku', 'description'])
        def get_products(search_result: SearchResult):
            return jsonify(search_result.to_dict())
    """
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            params = SearchRequestParser.parse(
                search_fields=search_fields, max_page_size=max_page_size
            )

            # Apply default sort if no sort specified
            if not params.sort and default_sort:
                if default_sort.startswith("-"):
                    params.sort = [SortConfig(field=default_sort[1:], direction="desc")]
                else:
                    params.sort = [SortConfig(field=default_sort, direction="asc")]

            result = SearchService.search(model, params)

            # Pass result to the route function
            return func(search_result=result, *args, **kwargs)

        return wrapper

    return decorator


__all__ = [
    "SearchService",
    "SearchRequestParser",
    "SearchParams",
    "SearchResult",
    "SearchFilter",
    "SortConfig",
    "FilterOperator",
    "searchable",
]
