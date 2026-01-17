#!/usr/bin/env python3
# FILE: scripts/generate_db_schema_doc.py | PURPOSE: Generate database schema documentation | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Database Schema Documentation Generator

This script analyzes the Django models and generates comprehensive database schema documentation
including tables, fields, relationships, indexes, and constraints.

Usage:
    python scripts/generate_db_schema_doc.py
"""

import os
import sys
import django
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
sys.path.insert(0, str(PROJECT_ROOT))

# Setup Django - use dev settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings.dev')
django.setup()

from django.apps import apps
from django.db import connection


def generate_schema_doc():
    """Generate comprehensive database schema documentation."""

    output = []
    output.append("# DATABASE SCHEMA DOCUMENTATION - Gaara ERP v12\n")
    output.append("**Generated**: 2025-11-18\n")
    output.append("**Database**: SQLite (development)\n")
    output.append("**Django Version**: 5.x\n")
    output.append("\n---\n\n")

    # Get all models
    all_models = apps.get_models()

    # Group by app
    apps_dict = {}
    for model in all_models:
        app_label = model._meta.app_label
        if app_label not in apps_dict:
            apps_dict[app_label] = []
        apps_dict[app_label].append(model)

    # Generate documentation for each app
    for app_label in sorted(apps_dict.keys()):
        output.append(f"## {app_label}\n\n")

        models = sorted(apps_dict[app_label], key=lambda m: m._meta.model_name)

        for model in models:
            output.append(f"### {model.__name__}\n\n")
            output.append(f"**Table**: `{model._meta.db_table}`\n\n")

            # Fields
            output.append("**Fields**:\n\n")
            output.append("| Field | Type | Null | Default | Index |\n")
            output.append("|-------|------|------|---------|-------|\n")

            for field in model._meta.get_fields():
                if hasattr(field, 'column'):
                    field_type = field.get_internal_type()
                    null = "Yes" if field.null else "No"
                    default = str(field.default) if field.has_default() else "-"
                    index = "Yes" if field.db_index else "No"
                    output.append(f"| {field.name} | {field_type} | {null} | {default} | {index} |\n")

            output.append("\n")

            # Foreign Keys
            fks = [f for f in model._meta.get_fields() if f.many_to_one and f.related_model]
            if fks:
                output.append("**Foreign Keys**:\n\n")
                for fk in fks:
                    related_model = fk.related_model._meta.label
                    output.append(f"- `{fk.name}` → {related_model}\n")
                output.append("\n")

            # Reverse Relations
            reverse_rels = [f for f in model._meta.get_fields() if f.one_to_many or f.one_to_one]
            if reverse_rels:
                output.append("**Reverse Relations**:\n\n")
                for rel in reverse_rels:
                    output.append(f"- `{rel.name}` (from {rel.related_model._meta.label})\n")
                output.append("\n")

            # Indexes
            if model._meta.indexes:
                output.append("**Indexes**:\n\n")
                for index in model._meta.indexes:
                    fields = ", ".join(index.fields)
                    output.append(f"- {index.name}: ({fields})\n")
                output.append("\n")

            # Unique Together
            if model._meta.unique_together:
                output.append("**Unique Together**:\n\n")
                for unique in model._meta.unique_together:
                    fields = ", ".join(unique)
                    output.append(f"- ({fields})\n")
                output.append("\n")

            output.append("---\n\n")

    # Write to file
    output_file = PROJECT_ROOT.parent / 'docs' / 'DB_Schema.md'
    output_file.write_text(''.join(output), encoding='utf-8')

    print(f"✓ Database schema documentation generated: {output_file}")
    print(f"✓ Total apps: {len(apps_dict)}")
    print(f"✓ Total models: {len(all_models)}")

    return output_file


def analyze_duplicates():
    """Analyze duplicate tables in the database."""

    print("\n" + "="*80)
    print("ANALYZING DUPLICATE TABLES")
    print("="*80)

    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]

        # Look for duplicate patterns
        duplicates = {}
        for table in tables:
            # Check for common duplicate patterns
            if 'company' in table.lower():
                if 'company' not in duplicates:
                    duplicates['company'] = []
                duplicates['company'].append(table)
            elif 'user' in table.lower():
                if 'user' not in duplicates:
                    duplicates['user'] = []
                duplicates['user'].append(table)
            elif 'invoice' in table.lower():
                if 'invoice' not in duplicates:
                    duplicates['invoice'] = []
                duplicates['invoice'].append(table)

        print("\nPotential Duplicate Tables:\n")
        for pattern, table_list in duplicates.items():
            if len(table_list) > 1:
                print(f"{pattern.upper()} tables ({len(table_list)}):")
                for table in table_list:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    print(f"  - {table}: {count} rows")
                print()


if __name__ == "__main__":
    try:
        output_file = generate_schema_doc()
        analyze_duplicates()
        print("\n✓ Schema documentation complete!")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

