/**
 * Common Components Index
 * @file frontend/src/components/common/index.js
 * 
 * تصدير جميع المكونات المشتركة
 */

// Print Components
export {
  PrintButton,
  PrintArea,
  usePrint
} from './PrintButton';

// Status Badge Components
export {
  StatusBadge,
  StockStatusBadge,
  PaymentStatusBadge,
  LotExpiryBadge,
  OnlineStatusBadge
} from './StatusBadge';

// Date Picker Components
export {
  DateRangePicker,
  SimpleDatePicker,
  MonthYearPicker
} from './DateRangePicker';

// Search Components
export {
  SearchInput,
  SearchWithSuggestions,
  GlobalSearch
} from './SearchInput';

// Dialog Components
export {
  ConfirmDialog,
  DeleteConfirmDialog,
  ConfirmProvider,
  useConfirm,
  useQuickConfirm
} from './ConfirmDialog';
