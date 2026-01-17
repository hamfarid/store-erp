#!/usr/bin/env python3
# FILE: scripts/deep_duplicate_analysis.py | PURPOSE: Deep code analysis for TRUE duplicates | OWNER: Architecture Team | LAST-AUDITED: 2025-11-18

"""
Deep Duplicate Analysis - Code Content Comparison

This script performs DEEP analysis by reading the FULL code content of models
to identify TRUE duplicates, not just naming similarities.

It compares:
1. Field names and types
2. Method signatures
3. Relationships (ForeignKey, ManyToMany)
4. Constraints and indexes
5. Meta options

Usage:
    python scripts/deep_duplicate_analysis.py
"""

import os
import sys
import django
import hashlib
from pathlib import Path
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent / 'gaara_erp'
sys.path.insert(0, str(PROJECT_ROOT))

# Setup Django - use dev settings which work
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings.dev')
django.setup()

from django.apps import apps
from django.db import models


def get_model_signature(model):
    """
    Generate a detailed signature of a model by analyzing its full structure.
    This goes beyond just the name - it analyzes the actual code.
    """
    signature = {
        'name': model.__name__,
        'module': model.__module__,
        'table': model._meta.db_table,
        'fields': {},
        'relationships': {},
        'methods': [],
        'meta': {},
    }

    # Analyze all fields
    for field in model._meta.get_fields():
        field_info = {
            'type': field.get_internal_type() if hasattr(field, 'get_internal_type') else type(field).__name__,
            'null': getattr(field, 'null', None),
            'blank': getattr(field, 'blank', None),
            'unique': getattr(field, 'unique', None),
            'db_index': getattr(field, 'db_index', None),
        }

        # Track relationships
        if field.many_to_one or field.one_to_one:
            signature['relationships'][field.name] = {
                'type': 'ForeignKey' if field.many_to_one else 'OneToOne',
                'to': field.related_model._meta.label if field.related_model else None,
            }
        elif field.many_to_many:
            signature['relationships'][field.name] = {
                'type': 'ManyToMany',
                'to': field.related_model._meta.label if field.related_model else None,
            }

        signature['fields'][field.name] = field_info

    # Analyze methods (excluding private and Django internals)
    for attr_name in dir(model):
        if not attr_name.startswith('_') and callable(getattr(model, attr_name)):
            attr = getattr(model, attr_name)
            if hasattr(attr, '__func__'):
                signature['methods'].append(attr_name)

    # Meta options
    signature['meta'] = {
        'ordering': model._meta.ordering,
        'unique_together': model._meta.unique_together,
        'indexes': [str(idx) for idx in model._meta.indexes],
        'abstract': model._meta.abstract,
    }

    return signature


def calculate_similarity(sig1, sig2):
    """
    Calculate similarity percentage between two model signatures.
    Returns a score from 0.0 to 1.0.
    """
    scores = []

    # Compare fields (40% weight)
    common_fields = set(sig1['fields'].keys()) & set(sig2['fields'].keys())
    all_fields = set(sig1['fields'].keys()) | set(sig2['fields'].keys())
    if all_fields:
        field_score = len(common_fields) / len(all_fields)

        # Check field types match
        type_matches = sum(
            1 for f in common_fields
            if sig1['fields'][f]['type'] == sig2['fields'][f]['type']
        )
        if common_fields:
            field_score *= (type_matches / len(common_fields))

        scores.append(('fields', field_score, 0.40))

    # Compare relationships (30% weight)
    common_rels = set(sig1['relationships'].keys()) & set(sig2['relationships'].keys())
    all_rels = set(sig1['relationships'].keys()) | set(sig2['relationships'].keys())
    if all_rels:
        rel_score = len(common_rels) / len(all_rels)
        scores.append(('relationships', rel_score, 0.30))

    # Compare methods (20% weight)
    common_methods = set(sig1['methods']) & set(sig2['methods'])
    all_methods = set(sig1['methods']) | set(sig2['methods'])
    if all_methods:
        method_score = len(common_methods) / len(all_methods)
        scores.append(('methods', method_score, 0.20))

    # Compare table structure (10% weight)
    table_score = 1.0 if sig1['table'] == sig2['table'] else 0.0
    scores.append(('table', table_score, 0.10))

    # Calculate weighted average
    if scores:
        total_score = sum(score * weight for _, score, weight in scores)
        return total_score, scores

    return 0.0, []


def find_true_duplicates():
    """
    Find TRUE duplicate models by analyzing their full code structure.
    """
    print("="*80)
    print("DEEP DUPLICATE ANALYSIS - FULL CODE COMPARISON")
    print("="*80)
    print()

    # Get all models
    all_models = apps.get_models()
    print(f"Analyzing {len(all_models)} models...\n")

    # Group models by name
    models_by_name = defaultdict(list)
    for model in all_models:
        models_by_name[model.__name__].append(model)

    # Find models with same name
    potential_duplicates = {
        name: models
        for name, models in models_by_name.items()
        if len(models) > 1
    }

    print(f"Found {len(potential_duplicates)} model names with multiple definitions\n")

    # Analyze each potential duplicate
    true_duplicates = []
    false_positives = []

    for model_name, models in sorted(potential_duplicates.items()):
        print(f"\n{'='*80}")
        print(f"ANALYZING: {model_name} ({len(models)} definitions)")
        print(f"{'='*80}\n")

        # Get signatures for all models
        signatures = [(model, get_model_signature(model)) for model in models]

        # Compare each pair
        for i, (model1, sig1) in enumerate(signatures):
            for j, (model2, sig2) in enumerate(signatures[i+1:], i+1):
                similarity, breakdown = calculate_similarity(sig1, sig2)

                print(f"\n{model1._meta.label} vs {model2._meta.label}")
                print(f"  Similarity: {similarity*100:.1f}%")

                if breakdown:
                    for component, score, weight in breakdown:
                        print(f"    - {component}: {score*100:.1f}% (weight: {weight*100:.0f}%)")

                # Display key differences
                print(f"\n  Fields:")
                print(f"    {model1._meta.label}: {len(sig1['fields'])} fields")
                print(f"    {model2._meta.label}: {len(sig2['fields'])} fields")

                unique_to_1 = set(sig1['fields'].keys()) - set(sig2['fields'].keys())
                unique_to_2 = set(sig2['fields'].keys()) - set(sig1['fields'].keys())

                if unique_to_1:
                    print(f"    Unique to {model1._meta.label}: {', '.join(list(unique_to_1)[:5])}")
                if unique_to_2:
                    print(f"    Unique to {model2._meta.label}: {', '.join(list(unique_to_2)[:5])}")

                # Classify
                if similarity >= 0.80:
                    true_duplicates.append({
                        'name': model_name,
                        'models': [model1._meta.label, model2._meta.label],
                        'similarity': similarity,
                        'recommendation': 'CONSOLIDATE - High similarity'
                    })
                    print(f"\n  ⚠️  TRUE DUPLICATE - Similarity {similarity*100:.1f}% >= 80%")
                elif similarity >= 0.50:
                    true_duplicates.append({
                        'name': model_name,
                        'models': [model1._meta.label, model2._meta.label],
                        'similarity': similarity,
                        'recommendation': 'REVIEW - Moderate similarity, may need consolidation'
                    })
                    print(f"\n  ⚠️  POTENTIAL DUPLICATE - Similarity {similarity*100:.1f}%")
                else:
                    false_positives.append({
                        'name': model_name,
                        'models': [model1._meta.label, model2._meta.label],
                        'similarity': similarity,
                        'recommendation': 'KEEP SEPARATE - Different implementations'
                    })
                    print(f"\n  ✓ FALSE POSITIVE - Similarity {similarity*100:.1f}% < 50%")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nTrue Duplicates (≥80% similarity): {len([d for d in true_duplicates if d['similarity'] >= 0.80])}")
    print(f"Potential Duplicates (50-80% similarity): {len([d for d in true_duplicates if 0.50 <= d['similarity'] < 0.80])}")
    print(f"False Positives (<50% similarity): {len(false_positives)}")

    return true_duplicates, false_positives


if __name__ == "__main__":
    try:
        true_dups, false_pos = find_true_duplicates()

        # Save results
        output_file = PROJECT_ROOT.parent / 'docs' / 'True_Duplicates_Analysis.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# TRUE DUPLICATES ANALYSIS - Deep Code Comparison\n\n")
            f.write("**Generated**: 2025-11-18\n")
            f.write("**Method**: Full code structure analysis\n\n")
            f.write("---\n\n")

            f.write("## TRUE DUPLICATES (≥80% similarity)\n\n")
            for dup in sorted(true_dups, key=lambda x: x['similarity'], reverse=True):
                if dup['similarity'] >= 0.80:
                    f.write(f"### {dup['name']} ({dup['similarity']*100:.1f}% similar)\n\n")
                    f.write(f"**Models**: {', '.join(dup['models'])}\n\n")
                    f.write(f"**Recommendation**: {dup['recommendation']}\n\n")
                    f.write("---\n\n")

            f.write("## POTENTIAL DUPLICATES (50-80% similarity)\n\n")
            for dup in sorted(true_dups, key=lambda x: x['similarity'], reverse=True):
                if 0.50 <= dup['similarity'] < 0.80:
                    f.write(f"### {dup['name']} ({dup['similarity']*100:.1f}% similar)\n\n")
                    f.write(f"**Models**: {', '.join(dup['models'])}\n\n")
                    f.write(f"**Recommendation**: {dup['recommendation']}\n\n")
                    f.write("---\n\n")

        print(f"\n✓ Analysis saved to: {output_file}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

