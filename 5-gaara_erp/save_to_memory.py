#!/usr/bin/env python3
"""Save initialization to memory system."""

import json
from pathlib import Path
from datetime import datetime

# Memory directory
memory_dir = Path.home() / '.global' / 'memory'

# Create decision entry
decision = {
    "timestamp": datetime.now().isoformat(),
    "type": "initialization_complete",
    "project": "Store ERP",
    "decision": "Memory and MCP systems initialized successfully",
    "components": {
        "memory": str(memory_dir),
        "mcp": str(Path.home() / '.global' / 'mcp'),
        "sentry_active": True,
        "sentry_org": "gaara-group",
        "sentry_user": "hamfarid",
        "sentry_user_id": 3918216
    },
    "environment_separation": {
        "helper_tools": str(Path.home() / '.global'),
        "project": "D:\\APPS_AI\\store\\Store",
        "verified": True
    },
    "mcp_servers": {
        "active": ["sentry"],
        "available": ["cloudflare", "playwright", "github"],
        "configuration": str(Path.home() / '.global' / 'mcp' / 'config' / 'mcp_config.json')
    },
    "next_actions": [
        "Use memory for all important decisions",
        "Check MCP servers before starting tasks",
        "Maintain environment separation",
        "Track progress in memory/state/",
        "Save learnings to memory/knowledge/"
    ],
    "lessons_learned": [
        "Environment separation is critical (helper tools vs project)",
        "Memory enables context retention across sessions",
        "MCP provides access to external tools",
        "Sentry MCP is active and ready for error monitoring"
    ]
}

# Save decision
decisions_dir = memory_dir / 'decisions'
decisions_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
decision_file = decisions_dir / f'init_{timestamp}.json'

with open(decision_file, 'w') as f:
    json.dump(decision, f, indent=2)

print(f"✅ Saved to memory: {decision_file}")

# Create knowledge entry
knowledge = {
    "timestamp": datetime.now().isoformat(),
    "type": "project_knowledge",
    "project": "Store ERP",
    "knowledge": {
        "project_name": "Store",
        "project_type": "ERP System - Arabic Inventory Management",
        "location": "D:\\APPS_AI\\store\\Store",
        "technologies": {
            "backend": "Flask (Python)",
            "frontend": "React + Vite",
            "database": "SQLite",
            "deployment": "Docker"
        },
        "features": [
            "Product Management",
            "Customer Management",
            "Supplier Management",
            "Inventory Tracking",
            "Sales Management",
            "Purchase Management",
            "Reporting & Analytics"
        ],
        "characteristics": {
            "rtl_support": True,
            "language": "Arabic",
            "status": "production"
        }
    },
    "helper_tools": {
        "memory_location": str(memory_dir),
        "mcp_location": str(Path.home() / '.global' / 'mcp'),
        "sentry_integration": True
    }
}

# Save knowledge
knowledge_dir = memory_dir / 'knowledge'
knowledge_dir.mkdir(parents=True, exist_ok=True)

knowledge_file = knowledge_dir / 'store_erp_project.json'

with open(knowledge_file, 'w', encoding='utf-8') as f:
    json.dump(knowledge, f, indent=2, ensure_ascii=False)

print(f"✅ Saved to memory: {knowledge_file}")

print("\n🎯 Memory system is now tracking Store ERP project!")

