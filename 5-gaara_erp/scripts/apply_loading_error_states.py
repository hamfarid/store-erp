#!/usr/bin/env python3
"""
Apply Enhanced Loading and Error States
Replaces old loading/error patterns with new enhanced components

Date: 2025-01-25
Phase: 2 - Component Improvements
"""

import os
import re
from pathlib import Path

# Components to update
COMPONENTS = [
    'frontend/src/components/Customers.jsx',
    'frontend/src/components/Suppliers.jsx',
    'frontend/src/components/InvoiceManagementComplete.jsx',
    'frontend/src/components/WarehouseManagement.jsx',
    'frontend/src/components/CategoryManagement.jsx',
    'frontend/src/components/CashBoxManagement.jsx',
    'frontend/src/components/SupplierDetails.jsx',
    # Phase 3: Missing components
    'frontend/src/components/PurchaseInvoiceManagement.jsx',
    'frontend/src/components/CurrencyManagement.jsx',
    'frontend/src/components/PaymentVouchers.jsx',
    'frontend/src/components/ProfitLossReport.jsx',
    'frontend/src/components/SecurityMonitoring.jsx',
    'frontend/src/components/ImportExport.jsx',
]

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write file content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_loading_state(content):
    """Replace old loading patterns with LoadingState"""
    
    # Pattern 1: if (loading) return <LoadingSpinner />
    pattern1 = r"if\s*\(\s*loading\s*\)\s*return\s*<LoadingSpinner\s*/>"
    replacement1 = "if (loading) return <LoadingState message=\"جاري التحميل...\" />"
    content = re.sub(pattern1, replacement1, content)
    
    # Pattern 2: if (loading) return <div>Loading...</div>
    pattern2 = r"if\s*\(\s*loading\s*\)\s*return\s*<div[^>]*>.*?Loading.*?</div>"
    replacement2 = "if (loading) return <LoadingState message=\"جاري التحميل...\" />"
    content = re.sub(pattern2, replacement2, content, flags=re.IGNORECASE)
    
    # Pattern 3: {loading && <LoadingSpinner />}
    pattern3 = r"{\s*loading\s*&&\s*<LoadingSpinner\s*/>\s*}"
    replacement3 = "{loading && <LoadingState message=\"جاري التحميل...\" />}"
    content = re.sub(pattern3, replacement3, content)
    
    return content

def replace_error_state(content):
    """Replace old error patterns with ErrorState"""
    
    # Pattern 1: if (error) return <div>Error: {error}</div>
    pattern1 = r"if\s*\(\s*error\s*\)\s*return\s*<div[^>]*>.*?Error.*?{error}.*?</div>"
    replacement1 = "if (error) return <ErrorState message={error} onRetry={loadData} />"
    content = re.sub(pattern1, replacement1, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Pattern 2: if (error) return <div className="error">{error}</div>
    pattern2 = r"if\s*\(\s*error\s*\)\s*return\s*<div[^>]*className=['\"]error['\"][^>]*>.*?{error}.*?</div>"
    replacement2 = "if (error) return <ErrorState message={error} onRetry={loadData} />"
    content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    return content

def add_empty_state(content):
    """Add EmptyState for empty data arrays"""
    
    # Pattern: if (data.length === 0) return <div>No data</div>
    # This is more complex and needs manual review
    # For now, we'll just add a comment
    
    return content

def replace_toast_calls(content):
    """Replace react-hot-toast import with EnhancedToast"""
    
    # Already done in previous script, but ensure consistency
    content = re.sub(
        r"import\s+toast\s+from\s+['\"]react-hot-toast['\"]",
        "import toast from './ui/EnhancedToast'",
        content
    )
    
    # Replace { toast } from 'react-hot-toast'
    content = re.sub(
        r"import\s+{\s*toast\s*}\s+from\s+['\"]react-hot-toast['\"]",
        "import toast from './ui/EnhancedToast'",
        content
    )
    
    return content

def replace_alert_with_toast(content):
    """Replace alert() calls with toast notifications"""
    
    # Pattern: alert('success message')
    success_pattern = r"alert\(['\"]تم ([^'\"]+) بنجاح['\"]\)"
    content = re.sub(
        success_pattern,
        r"toast.success('تم \1 بنجاح')",
        content
    )
    
    # Pattern: alert('error message')
    error_pattern = r"alert\(['\"]حدث خطأ ([^'\"]+)['\"]\)"
    content = re.sub(
        error_pattern,
        r"toast.error('حدث خطأ \1')",
        content
    )
    
    # Pattern: alert('generic message')
    generic_pattern = r"alert\(['\"]([^'\"]+)['\"]\)"
    content = re.sub(
        generic_pattern,
        r"toast.info('\1')",
        content
    )
    
    return content

def process_component(filepath):
    """Process a single component file"""
    print(f"Processing: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"  ⚠️  File not found: {filepath}")
        return False
    
    try:
        content = read_file(filepath)
        original_content = content
        
        # Apply transformations
        content = replace_loading_state(content)
        content = replace_error_state(content)
        content = replace_toast_calls(content)
        content = replace_alert_with_toast(content)
        
        # Only write if changed
        if content != original_content:
            write_file(filepath, content)
            print(f"  ✅ Updated successfully")
            return True
        else:
            print(f"  ℹ️  No changes needed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Applying Enhanced Loading/Error States")
    print("=" * 60)
    print()
    
    updated_count = 0
    
    for component in COMPONENTS:
        if process_component(component):
            updated_count += 1
        print()
    
    print("=" * 60)
    print(f"Summary: {updated_count}/{len(COMPONENTS)} components updated")
    print("=" * 60)

if __name__ == '__main__':
    main()

