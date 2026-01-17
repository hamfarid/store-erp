# FILE: backend/src/routes/rag.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

# type: ignore
# flake8: noqa
# RAG endpoint backed by rag_service
from flask import Blueprint, request, jsonify

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

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
def rag_query():
    data = request.get_json(silent=True) or {}
    q = data.get("query", "")
    top_k = data.get("top_k")
    result = rag_query_service(q, top_k=top_k)
    status = 200 if result.get("success") else 400
    return jsonify(result), status
