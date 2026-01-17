"""
File: config/definitions/custom.py
Project-specific custom definitions

Add your project-specific enums, types, and classes here.
"""

from enum import Enum


# ============================================================================
# Project-Specific Enums
# ============================================================================

class ProjectStatus(str, Enum):
    """Project status"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    """Priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    BLOCKED = "blocked"


# ============================================================================
# Export
# ============================================================================

__all__ = [
    'ProjectStatus',
    'Priority',
    'TaskStatus',
]
