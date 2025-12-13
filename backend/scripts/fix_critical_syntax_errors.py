# FILE: backend/scripts/fix_critical_syntax_errors.py | PURPOSE: Fix critical syntax errors in route files | OWNER: Backend | RELATED: routes/*.py | LAST-AUDITED: 2025-10-25

"""
Fix critical syntax errors in route files
Specifically targets the pattern:
    return success_response(data=X,
        'message': f'...',
        'fallback': True
    }), 201
"""

import re
from pathlib import Path

routes_dir = Path(__file__).parent.parent / "src" / "routes"
route_files = list(routes_dir.glob("*.py"))

print(f"Scanning {len(route_files)} route files for critical syntax errors...")
print()

fixed_count = 0

for route_file in route_files:
    try:
        content = route_file.read_text(encoding="utf-8")
        original_content = content

        # Pattern 1: return success_response(data=X,\n        'message': f'...{str(error)[:50], message='Success', status_code=200)',\n        'fallback': True\n    }), 201
        pattern1 = r"return success_response\(data=([^,\n]+),\s*\n\s*'message':\s*f'([^']+)\{str\(([^)]+)\)\[:50\],\s*message='Success',\s*status_code=200\)',\s*\n\s*'fallback':\s*True\s*\n\s*\}\),\s*201"

        def fix_pattern1(match):
            data_var = match.group(1)
            message_prefix = match.group(2)
            error_var = match.group(3)

            # Determine entity type from message
            if "عميل" in message_prefix or "customer" in message_prefix.lower():
                entity = "customer"
                entity_ar = "العميل"
            elif "مورد" in message_prefix or "supplier" in message_prefix.lower():
                entity = "supplier"
                entity_ar = "المورد"
            elif "منتج" in message_prefix or "product" in message_prefix.lower():
                entity = "product"
                entity_ar = "المنتج"
            else:
                entity = "item"
                entity_ar = "العنصر"

            return f"""return success_response(
                data={{
                    '{entity}': {data_var},
                    'fallback': True
                }},
                message=f'تم إنشاء {entity_ar} تجريبياً / {entity.capitalize()} created (fallback): {{str({error_var})[:50]}}',
                status_code=201
            )"""

        content = re.sub(pattern1, fix_pattern1, content)

        # Pattern 2: return success_response(data=X,\n        'total': ...,\n        'message': f'...{str(error)[:100], message='Success', status_code=200)',\n        'fallback': True\n    })
        pattern2 = r"return success_response\(data=([^,\n]+),\s*\n\s*'total':\s*len\(([^)]+)\),\s*\n\s*'message':\s*f'([^']+)\{str\(([^)]+)\)\[:100\],\s*message='Success',\s*status_code=200\)',\s*\n\s*'fallback':\s*True\s*\n\s*\}\)"

        def fix_pattern2(match):
            data_var = match.group(1)
            total_var = match.group(2)
            message_prefix = match.group(3)
            error_var = match.group(4)

            # Determine entity type
            if "عملاء" in message_prefix or "customers" in message_prefix.lower():
                entity = "customers"
            elif "موردين" in message_prefix or "suppliers" in message_prefix.lower():
                entity = "suppliers"
            elif "منتجات" in message_prefix or "products" in message_prefix.lower():
                entity = "products"
            else:
                entity = "items"

            return f"""return success_response(
                data={{
                    '{entity}': {data_var},
                    'total': len({total_var}),
                    'fallback': True
                }},
                message=f'بيانات تجريبية / Sample data: {{str({error_var})[:50]}}',
                status_code=200
            )"""

        content = re.sub(pattern2, fix_pattern2, content)

        # Check if modified
        if content != original_content:
            route_file.write_text(content, encoding="utf-8")
            print(f"✅ Fixed: {route_file.name}")
            fixed_count += 1

    except Exception as e:
        print(f"❌ Error in {route_file.name}: {e}")

print()
print("=" * 80)
print(f"✅ Fixed {fixed_count} files")
print("=" * 80)
