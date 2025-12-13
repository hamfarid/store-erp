# FILE: backend/src/routes/rag.py | PURPOSE: Routes with P0.2.4 error
# envelope | OWNER: Backend | RELATED:
# middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-12-01

# type: ignore
# flake8: noqa
# RAG endpoint backed by rag_service
from flask import Blueprint, request, jsonify, g
from marshmallow import Schema, fields, validate, EXCLUDE

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)


# P0.20: RAG Input Validation Schema
class RAGQuerySchema(Schema):
    """P0.20: Schema for validating RAG query requests"""

    class Meta:
        unknown = EXCLUDE

    query = fields.Str(
        required=True,
        validate=[
            validate.Length(
                min=1, max=2000, error="Query must be between 1 and 2000 characters"
            )
        ],
    )
    top_k = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1, max=50, error="top_k must be between 1 and 50"),
    )


# P0.20: Import validation decorator
try:
    from src.utils.validation import validate_json, sanitize_string
except ImportError:

    def validate_json(schema):
        def decorator(f):
            return f

        return decorator

    def sanitize_string(s):
        return s if s else ""


try:
    from rag_service import query as rag_query_service

    RAG_AVAILABLE = True
except ImportError:
    # Fallback for different import paths
    try:
        import sys
        import os

        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        RAG_AVAILABLE = True
    except ImportError:
        # RAG service not available, create a mock function
        def rag_query_service(query, top_k=None):
            return {
                "success": False,
                "error": "RAG service not available - chromadb dependencies not installed",
                "query": query,
                "results": [],
            }

        RAG_AVAILABLE = False

rag_bp = Blueprint("rag_bp", __name__)


@rag_bp.route("/rag/query", methods=["POST"])
@validate_json(RAGQuerySchema)
def rag_query():
    """
    P0.20: RAG query endpoint with input validation

    Accepts:
        query: string (1-2000 chars) - The search query
        top_k: int (1-50, optional) - Number of results to return

    Returns:
        RAG search results or error
    """
    # Use validated data from decorator
    data = getattr(g, "validated_data", None) or request.get_json(silent=True) or {}

    # Sanitize the query string for additional safety
    q = sanitize_string(data.get("query", ""))
    top_k = data.get("top_k")

    # Validate query is not empty after sanitization
    if not q or not q.strip():
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Query cannot be empty",
                    "code": "VALIDATION_ERROR",
                }
            ),
            400,
        )

    result = rag_query_service(q.strip(), top_k=top_k)
    status = 200 if result.get("success") else 400
    return jsonify(result), status
