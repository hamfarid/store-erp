# FILE: backend/scripts/fix_unified_routes_syntax.py | PURPOSE: Fix syntax errors in *_unified.py route files | OWNER: Backend | RELATED: routes/*_unified.py | LAST-AUDITED: 2025-10-25

"""
Fix syntax errors in *_unified.py route files
Specifically targets the pattern:
    return success_response(data=new_item,
        'message': f'...',
        'fallback': True
    ), 201
"""

import re
from pathlib import Path

routes_dir = Path(__file__).parent.parent / "src" / "routes"
unified_files = list(routes_dir.glob("*_unified.py"))

print(f"Scanning {len(unified_files)} *_unified.py files for syntax errors...")
print()

fixed_count = 0

for route_file in unified_files:
    try:
        content = route_file.read_text(encoding="utf-8")
        original_content = content

        # Pattern: return success_response(data=X,\n            'message': ..., message='Success', status_code=200)
        # Fix by converting to proper dict format

        # Find all occurrences of the broken pattern
        lines = content.split("\n")
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check if this line starts a broken success_response call
            if "return success_response(data=" in line and line.strip().endswith(","):
                # This might be a broken pattern
                # Collect the full call
                call_lines = [line]
                j = i + 1
                paren_count = line.count("(") - line.count(")")

                while j < len(lines) and paren_count > 0:
                    call_lines.append(lines[j])
                    paren_count += lines[j].count("(") - lines[j].count(")")
                    j += 1

                full_call = "\n".join(call_lines)

                # Check if it has the broken pattern (positional args after keyword args)
                if "'message':" in full_call or "'fallback':" in full_call:
                    # Extract data variable
                    match = re.search(r"data=([^,\n]+),", full_call)
                    if match:
                        data_var = match.group(1).strip()

                        # Determine entity type
                        if "partner" in route_file.name.lower():
                            entity = "partner"
                            entity_ar = "الشريك"
                        elif "product" in route_file.name.lower():
                            entity = "product"
                            entity_ar = "المنتج"
                        else:
                            entity = "item"
                            entity_ar = "العنصر"

                        # Get indentation
                        indent = len(line) - len(line.lstrip())
                        indent_str = " " * indent

                        # Create fixed version
                        fixed_call = f"""{indent_str}return success_response(
{indent_str}    data={{
{indent_str}        '{entity}': {data_var},
{indent_str}        'fallback': True
{indent_str}    }},
{indent_str}    message='تم إنشاء {entity_ar} تجريبياً / {entity.capitalize()} created (fallback)',
{indent_str}    status_code=201
{indent_str})"""

                        fixed_lines.append(fixed_call)
                        i = j
                        continue

                # Not a broken pattern, keep as is
                fixed_lines.append(line)
                i += 1
            else:
                fixed_lines.append(line)
                i += 1

        content = "\n".join(fixed_lines)

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
