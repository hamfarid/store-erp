# FILE: backend/scripts/fix_temp_api_syntax.py | PURPOSE: Fix syntax errors in temp_api.py | OWNER: Backend | RELATED: routes/temp_api.py | LAST-AUDITED: 2025-10-25

"""
Fix syntax errors in temp_api.py caused by incorrect success_response() calls
"""

import re
from pathlib import Path

# Path to temp_api.py
temp_api_path = Path(__file__).parent.parent / "src" / "routes" / "temp_api.py"

# Read file
content = temp_api_path.read_text(encoding="utf-8")

# Pattern to match broken success_response calls
# Matches: return success_response(data=SOMETHING,\n            'total': ...
pattern = r"return success_response\(data=([^,]+),\s*\n\s*'total':\s*len\(([^)]+)\),\s*\n\s*'message':\s*'([^']+)'\s*\n\s*,\s*message='Success',\s*status_code=200\)"


def replacement(match):
    data_var = match.group(1)
    total_var = match.group(2)
    arabic_message = match.group(3)

    # Determine English message based on Arabic
    if "فئات" in arabic_message:
        english = "Categories retrieved successfully"
        key = "categories"
    elif "مخازن" in arabic_message:
        english = "Warehouses retrieved successfully"
        key = "warehouses"
    elif "مخزون" in arabic_message:
        english = "Inventory retrieved successfully"
        key = "inventory"
    elif "تقارير" in arabic_message:
        english = "Reports retrieved successfully"
        key = "reports"
    else:
        english = "Data retrieved successfully"
        key = "data"

    return f"""return success_response(
            data={{
                '{key}': {data_var},
                'total': len({total_var})
            }},
            message='{arabic_message} / {english}',
            status_code=200
        )"""


# Replace all occurrences
content = re.sub(pattern, replacement, content)

# Also fix error_response calls
error_pattern = r"return error_response\(message='([^']+)',\s*code=ErrorCodes\.SYS_INTERNAL_ERROR,\s*status_code=500\)"


def error_replacement(match):
    arabic_message = match.group(1)
    return f"""return error_response(
            message=f'{arabic_message} / Error: {{str(e)}}',
            code=ErrorCodes.SYS_INTERNAL_ERROR,
            status_code=500
        )"""


content = re.sub(error_pattern, error_replacement, content)

# Write back
temp_api_path.write_text(content, encoding="utf-8")

print("✅ Fixed temp_api.py syntax errors")
