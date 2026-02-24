#!/usr/bin/env python3
"""
Apply UI Improvements to All Components
Automatically updates components to use enhanced UI states

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

def update_imports(content):
    """Update imports to include enhanced components"""
    
    # Check if already has enhanced imports
    if 'EnhancedStates' in content:
        return content
    
    # Find react-hot-toast import
    toast_pattern = r"import\s+{\s*toast\s*}\s+from\s+['\"]react-hot-toast['\"]"
    
    if re.search(toast_pattern, content):
        # Replace react-hot-toast with EnhancedToast
        content = re.sub(
            toast_pattern,
            "import toast from './ui/EnhancedToast'",
            content
        )
    
    # Add enhanced components import after lucide-react
    lucide_pattern = r"(import\s+{[^}]+}\s+from\s+['\"]lucide-react['\"])"
    
    enhanced_imports = """
// Enhanced UI Components
import { LoadingState, ErrorState, EmptyState } from './ui/EnhancedStates'
import ConfirmationDialog from './ui/ConfirmationDialog'"""
    
    if not re.search(r"import.*EnhancedStates", content):
        content = re.sub(
            lucide_pattern,
            r"\1" + enhanced_imports,
            content
        )
    
    return content

def add_delete_dialog_state(content):
    """Add state for delete confirmation dialog"""
    
    # Check if already has delete dialog state
    if 'showDeleteDialog' in content:
        return content
    
    # Find useState declarations
    state_pattern = r"(const\s+\[.*useState\(.*\))"
    
    # Add delete dialog states
    delete_states = """  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [itemToDelete, setItemToDelete] = useState(null)"""
    
    # Find last useState and add after it
    matches = list(re.finditer(state_pattern, content))
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        content = content[:insert_pos] + '\n' + delete_states + content[insert_pos:]
    
    return content

def replace_window_confirm(content):
    """Replace window.confirm with ConfirmationDialog"""
    
    # Pattern: if (window.confirm('...')) { ... }
    confirm_pattern = r"if\s*\(\s*window\.confirm\(['\"]([^'\"]+)['\"]\)\s*\)\s*{([^}]+)}"
    
    def replace_confirm(match):
        message = match.group(1)
        action = match.group(2).strip()
        
        # Extract function name from action
        func_match = re.search(r'(\w+)\(', action)
        if func_match:
            func_name = func_match.group(1)
            return f"""setItemToDelete(item);
    setShowDeleteDialog(true);"""
        
        return match.group(0)
    
    content = re.sub(confirm_pattern, replace_confirm, content, flags=re.DOTALL)
    
    return content

def add_confirmation_dialog_jsx(content):
    """Add ConfirmationDialog JSX at the end of component"""
    
    # Check if already has ConfirmationDialog
    if '<ConfirmationDialog' in content:
        return content
    
    # Find the last closing tag before export
    export_pattern = r"(export\s+default)"
    
    dialog_jsx = """
      {/* Delete Confirmation Dialog */}
      <ConfirmationDialog
        isOpen={showDeleteDialog}
        onClose={() => {
          setShowDeleteDialog(false);
          setItemToDelete(null);
        }}
        onConfirm={async () => {
          setIsDeleting(true);
          try {
            await handleDelete(itemToDelete);
            setShowDeleteDialog(false);
            setItemToDelete(null);
          } catch (error) {
            console.error(error);
          } finally {
            setIsDeleting(false);
          }
        }}
        title="تأكيد الحذف"
        message="هل أنت متأكد من حذف هذا العنصر؟ لا يمكن التراجع عن هذا الإجراء."
        variant="danger"
        requireConfirmation={true}
        confirmationText="حذف"
        isLoading={isDeleting}
      />
"""
    
    # Find last return statement closing
    return_pattern = r"(</div>\s*\)\s*;?\s*}\s*)(export\s+default)"
    
    content = re.sub(
        return_pattern,
        r"\1" + dialog_jsx + "\n\n\\2",
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
        content = update_imports(content)
        content = add_delete_dialog_state(content)
        content = replace_window_confirm(content)
        content = add_confirmation_dialog_jsx(content)
        
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
    print("Applying UI Improvements to Components")
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

