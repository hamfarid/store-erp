# Export Controls Component Guide

**FILE**: `frontend/src/components/ui/ExportControls.jsx`  
**PURPOSE**: Reusable export format selector and button component  
**OWNER**: Frontend Team  
**LAST-AUDITED**: 2025-10-29

## Overview

`ExportControls` is a unified, reusable React component that provides:
- Format selector (CSV/XLSX)
- Export button with loading state
- RBAC permission checks
- Consistent UI/UX across all export operations
- Activity logging integration

## Features

✅ **Format Selection**: Users can choose between CSV and XLSX formats  
✅ **Permission Guards**: Respects `canExport` permission from AuthContext  
✅ **Loading State**: Shows "جاري التصدير..." during export  
✅ **Error Handling**: Graceful error handling with console logging  
✅ **Customizable**: Supports custom formats, callbacks, and styling  
✅ **Activity Logging**: Automatically logs export actions  

## Installation

The component is already available at:
```
frontend/src/components/ui/ExportControls.jsx
```

## Usage

### Basic Usage

```jsx
import ExportControls from './ui/ExportControls'

function MyComponent() {
  const { hasPermission } = useAuth()
  const canExport = hasPermission('reports.export')
  
  const data = [
    { id: 1, name: 'Item 1', value: 100 },
    { id: 2, name: 'Item 2', value: 200 }
  ]

  return (
    <ExportControls
      data={data}
      filename="my-export"
      canExport={canExport}
    />
  )
}
```

### Advanced Usage with Callbacks

```jsx
<ExportControls
  data={filteredData}
  filename="users-report"
  canExport={canExport}
  formats={['CSV', 'XLSX', 'JSON']}
  className="ml-3"
  onBeforeExport={async (format) => {
    console.log(`Starting export in ${format} format`)
    // Custom pre-export logic
  }}
  onAfterExport={async (format) => {
    console.log(`Export completed in ${format} format`)
    // Custom post-export logic
  }}
/>
```

### With Tab-Based Data Selection

```jsx
<ExportControls
  data={
    activeTab === 'users' ? users :
    activeTab === 'roles' ? roles :
    activeTab === 'activities' ? activities : []
  }
  filename={
    activeTab === 'users' ? 'users' :
    activeTab === 'roles' ? 'roles' :
    activeTab === 'activities' ? 'activities' : 'export'
  }
  canExport={canExport}
/>
```

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `data` | `Array<Object>` | ✅ | - | Data to export |
| `filename` | `string` | ✅ | - | Base filename (without extension) |
| `canExport` | `boolean` | ✅ | - | Permission check result |
| `className` | `string` | ❌ | `''` | Additional CSS classes |
| `onBeforeExport` | `Function` | ❌ | `undefined` | Callback before export |
| `onAfterExport` | `Function` | ❌ | `undefined` | Callback after export |
| `formats` | `Array<string>` | ❌ | `['CSV', 'XLSX']` | Available export formats |

## Export Functions

The component uses two export utilities from `frontend/src/utils/export.js`:

### `exportToCSV(filename, rows, options)`
- Exports data to CSV format
- Includes UTF-8 BOM for Excel compatibility
- Automatically logs activity

### `exportToExcel(filename, rows, options)`
- Exports data to XLSX format
- Auto-sizes columns based on content
- Automatically logs activity

## Components Using ExportControls

✅ **UserManagementAdvanced.jsx** - User/Role/Activity export  
✅ **AccountingSystem.jsx** - Currency/Exchange Rate/Cash Box/Voucher export  
✅ **IntegratedReports.jsx** - Report export  

## Migration Guide

### Before (Manual Implementation)

```jsx
const [exportFormat, setExportFormat] = useState('CSV')

<select value={exportFormat} onChange={(e) => setExportFormat(e.target.value)}>
  <option value="CSV">CSV</option>
  <option value="XLSX">Excel</option>
</select>

<button onClick={() => {
  if (exportFormat === 'XLSX') {
    exportToExcel(filename, data)
  } else {
    exportToCSV(filename, data)
  }
}}>
  تصدير
</button>
```

### After (Using ExportControls)

```jsx
<ExportControls
  data={data}
  filename={filename}
  canExport={canExport}
/>
```

## Styling

The component uses Tailwind CSS classes and respects the design token system:
- **Active State**: `bg-green-600 hover:bg-green-700 active:bg-green-800`
- **Disabled State**: `bg-gray-400 cursor-not-allowed opacity-50`
- **Focus State**: `focus:outline-none focus:ring-2 focus:ring-blue-500`

## Activity Logging

All exports are automatically logged with:
- `action`: 'EXPORT'
- `entityType`: Derived from filename
- `format`: 'CSV' or 'XLSX'
- `recordCount`: Number of records exported
- `outcome`: 'success' or 'error'
- `timed_ms`: Export duration in milliseconds

## Error Handling

The component handles:
- Empty data arrays
- Missing permissions
- Export failures
- Network errors (via export utilities)

All errors are logged to console and displayed via toast notifications.

## Best Practices

1. **Always provide `canExport` permission check**
   ```jsx
   const { hasPermission } = useAuth()
   const canExport = hasPermission('reports.export')
   ```

2. **Use meaningful filenames**
   ```jsx
   filename="users-report-2025-10-29"  // ✅ Good
   filename="export"                    // ❌ Avoid
   ```

3. **Provide context-specific data**
   ```jsx
   // ✅ Good - data changes based on active tab
   data={activeTab === 'users' ? users : roles}
   
   // ❌ Avoid - always exports same data
   data={allData}
   ```

4. **Use callbacks for custom logic**
   ```jsx
   onBeforeExport={async (format) => {
     // Validate data, show confirmation, etc.
   }}
   ```

## Testing

Example test cases:
```javascript
describe('ExportControls', () => {
  it('should export CSV when CSV format is selected', () => {
    // Test implementation
  })

  it('should export XLSX when XLSX format is selected', () => {
    // Test implementation
  })

  it('should disable export when canExport is false', () => {
    // Test implementation
  })

  it('should show loading state during export', () => {
    // Test implementation
  })
})
```

## Troubleshooting

### Export button is disabled
- Check if `canExport` permission is granted
- Verify data array is not empty
- Ensure user has 'reports.export' permission

### File not downloading
- Check browser console for errors
- Verify filename is valid
- Check if pop-ups are blocked

### Wrong data exported
- Verify `data` prop is correctly filtered
- Check if `activeTab` state is updated
- Ensure data transformation logic is correct

## Future Enhancements

- [ ] Add PDF export support
- [ ] Add JSON export format
- [ ] Add batch export for multiple formats
- [ ] Add export scheduling
- [ ] Add export templates
- [ ] Add export history tracking

## Related Files

- `frontend/src/utils/export.js` - Export utility functions
- `frontend/src/contexts/AuthContext.jsx` - Authentication context
- `frontend/src/utils/activityLogger.js` - Activity logging
- `frontend/src/components/ui/EnhancedToast.jsx` - Toast notifications

