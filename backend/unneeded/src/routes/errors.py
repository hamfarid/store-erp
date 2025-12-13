# FILE: backend/src/routes/errors.py | PURPOSE: Routes with P0.2.4 error envelope | OWNER: Backend | RELATED: middleware/error_envelope_middleware.py | LAST-AUDITED: 2025-10-25

"""
Errors & Metrics Ingestion Blueprint
- POST /api/errors/report   (structured error events from frontend)
- POST /api/metrics/report  (aggregated performance metrics from frontend)

Accepts JSON payloads and logs them with traceId for correlation.
Keeps implementation minimal and storage-agnostic (logs only).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request

# P0.2.4: Import error envelope helpers
from src.middleware.error_envelope_middleware import (
    success_response,
    error_response,
    ErrorCodes,
)

errors_bp = Blueprint("errors", __name__)
logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_trace_id(payload: dict | None) -> str:
    header_tid = request.headers.get("X-Trace-Id")
    if header_tid:
        return header_tid
    if isinstance(payload, dict):
        tid = payload.get("traceId") or payload.get("trace_id")
        if tid:
            return str(tid)
    return str(uuid4())


@errors_bp.route("/api/errors/report", methods=["POST"])
def report_frontend_error():
    """Ingest structured frontend error events.

    Expected fields (tolerant):
    - message, stack, componentStack, timestamp, userAgent, url, userId,
      errorId, traceId, severity, route, details
    """
    # Allow both JSON and text/beacon payloads
    payload = request.get_json(silent=True)
    if payload is None:
        try:
            raw = request.get_data(as_text=True) or "{}"
            payload = json.loads(raw)
        except Exception:
            payload = {}

    trace_id = _get_trace_id(payload)
    server_trace_id = str(uuid4())

    record = {
        "type": "frontend_error",
        "received_at": _now_iso(),
        "remote_addr": getattr(request, "remote_addr", None),
        "user_agent": getattr(getattr(request, "user_agent", None), "string", None),
        "path": request.path,
        "traceId": trace_id,
        "serverTraceId": server_trace_id,
        "payload": payload or {},
    }

    # Basic validation
    if not payload or not payload.get("message"):
        logger.warning("[ErrorsIngest] Missing or invalid payload: %s", record)
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "INVALID_PAYLOAD",
                        "message": "Payload must include at least 'message'",
                        "traceId": trace_id,
                    },
                    "timestamp": _now_iso(),
                }
            ),
            400,
        )

    # Log with structured JSON for downstream collectors
    try:
        logger.error("FrontendError %s", json.dumps(record, ensure_ascii=False))
    except Exception:
        # Fallback to non-JSON logging if any issue
        logger.error("FrontendError %s", record)

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "received": "error",
                    "traceId": trace_id,
                    "serverTraceId": server_trace_id,
                },
                "message": "Error report ingested",
                "timestamp": _now_iso(),
            }
        ),
        201,
    )


@errors_bp.route("/api/metrics/report", methods=["POST"])
def report_frontend_metrics():
    """Ingest aggregated performance metrics from frontend (beacon-friendly)."""
    payload = request.get_json(silent=True)
    if payload is None:
        try:
            raw = request.get_data(as_text=True) or "{}"
            payload = json.loads(raw)
        except Exception:
            payload = {}

    trace_id = _get_trace_id(payload)
    server_trace_id = str(uuid4())

    record = {
        "type": "frontend_metrics",
        "received_at": _now_iso(),
        "remote_addr": getattr(request, "remote_addr", None),
        "path": request.path,
        "traceId": trace_id,
        "serverTraceId": server_trace_id,
        "payload": payload or {},
    }

    try:
        logger.info("FrontendMetrics %s", json.dumps(record, ensure_ascii=False))
    except Exception:
        logger.info("FrontendMetrics %s", record)

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "received": "metrics",
                    "traceId": trace_id,
                    "serverTraceId": server_trace_id,
                },
                "message": "Metrics ingested",
                "timestamp": _now_iso(),
            }
        ),
        201,
    )
