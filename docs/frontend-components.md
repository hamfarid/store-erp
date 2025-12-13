# 🎨 Frontend Components Documentation - توثيق مكونات الواجهة الأمامية

## 🏗️ هيكل المكونات

### 📁 src/components/
```
components/
├── 📂 common/              # المكونات المشتركة
│   ├── Button.jsx          # أزرار مخصصة
│   ├── Modal.jsx           # نوافذ منبثقة
│   ├── Table.jsx           # جداول البيانات
│   ├── Form.jsx            # نماذج الإدخال
│   ├── Loading.jsx         # مؤشرات التحميل
│   ├── Toast.jsx           # رسائل التنبيه
│   └── ErrorBoundary.js    # معالج الأخطاء
├── 📂 layout/              # مكونات التخطيط
│   ├── Header.jsx          # رأس الصفحة
│   ├── Sidebar.jsx         # الشريط الجانبي
│   ├── Footer.jsx          # تذييل الصفحة
│   └── Layout.jsx          # التخطيط الرئيسي
├── 📂 forms/               # نماذج متخصصة
│   ├── ProductForm.jsx     # نموذج المنتجات
│   ├── CustomerForm.jsx    # نموذج العملاء
│   ├── SalesForm.jsx       # نموذج المبيعات
│   └── PaymentForm.jsx     # نموذج المدفوعات
├── 📂 charts/              # الرسوم البيانية
│   ├── SalesChart.jsx      # رسم المبيعات
│   ├── InventoryChart.jsx  # رسم المخزون
│   └── FinancialChart.jsx  # الرسوم المالية
└── 📂 ui/                  # مكونات واجهة المستخدم
    ├── Card.jsx            # بطاقات العرض
    ├── Badge.jsx           # شارات الحالة
    ├── Dropdown.jsx        # قوائم منسدلة
    └── Pagination.jsx      # ترقيم الصفحات
```

## 🧩 المكونات الأساسية

### 🔘 Button Component
```jsx
import { Button } from '../components/common/Button'

// الاستخدام الأساسي
<Button variant="primary" size="md" onClick={handleClick}>
  حفظ
</Button>

// الخصائص المتاحة
variant: 'primary' | 'secondary' | 'success' | 'danger' | 'warning'
size: 'sm' | 'md' | 'lg'
disabled: boolean
loading: boolean
icon: ReactNode
```

### 📋 Table Component
```jsx
import { Table } from '../components/common/Table'

const columns = [
  { key: 'id', label: 'الرقم', sortable: true },
  { key: 'name', label: 'الاسم', sortable: true },
  { key: 'actions', label: 'الإجراءات', render: (row) => <Actions row={row} /> }
]

<Table 
  data={products}
  columns={columns}
  pagination={true}
  searchable={true}
  onSort={handleSort}
  onSearch={handleSearch}
/>
```

### 🪟 Modal Component
```jsx
import { Modal } from '../components/common/Modal'

<Modal 
  isOpen={isModalOpen}
  onClose={closeModal}
  title="إضافة منتج جديد"
  size="lg"
>
  <ProductForm onSubmit={handleSubmit} />
</Modal>
```

### 📝 Form Components
```jsx
import { Form, Input, Select, TextArea } from '../components/common/Form'

<Form onSubmit={handleSubmit} validation={validationSchema}>
  <Input 
    name="name"
    label="اسم المنتج"
    required
    placeholder="أدخل اسم المنتج"
  />
  
  <Select 
    name="category"
    label="الفئة"
    options={categories}
    required
  />
  
  <TextArea 
    name="description"
    label="الوصف"
    rows={4}
  />
</Form>
```

## 📊 مكونات الرسوم البيانية

### 📈 Sales Chart
```jsx
import { SalesChart } from '../components/charts/SalesChart'

<SalesChart 
  data={salesData}
  period="monthly"
  showComparison={true}
  height={400}
/>
```

### 📦 Inventory Chart
```jsx
import { InventoryChart } from '../components/charts/InventoryChart'

<InventoryChart 
  data={inventoryData}
  type="donut"
  showLegend={true}
/>
```

## 🎯 مكونات متخصصة

### 🛍️ Product Card
```jsx
import { ProductCard } from '../components/ui/ProductCard'

<ProductCard 
  product={product}
  onEdit={handleEdit}
  onDelete={handleDelete}
  onView={handleView}
  showActions={true}
/>
```

### 👤 Customer Card
```jsx
import { CustomerCard } from '../components/ui/CustomerCard'

<CustomerCard 
  customer={customer}
  showBalance={true}
  onContact={handleContact}
/>
```

### 🧾 Invoice Component
```jsx
import { Invoice } from '../components/forms/Invoice'

<Invoice 
  invoice={invoiceData}
  editable={true}
  onSave={handleSave}
  onPrint={handlePrint}
/>
```

## 🎨 مكونات التخطيط

### 🏠 Layout Component
```jsx
import { Layout } from '../components/layout/Layout'

<Layout>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/products" element={<Products />} />
  </Routes>
</Layout>
```

### 📱 Sidebar Component
```jsx
import { Sidebar } from '../components/layout/Sidebar'

<Sidebar 
  collapsed={isCollapsed}
  onToggle={toggleSidebar}
  menuItems={menuItems}
  userInfo={currentUser}
/>
```

### 🎯 Header Component
```jsx
import { Header } from '../components/layout/Header'

<Header 
  title="لوحة التحكم"
  showSearch={true}
  showNotifications={true}
  onSearch={handleSearch}
/>
```

## 🔧 مكونات الأدوات

### 🔍 Search Component
```jsx
import { Search } from '../components/common/Search'

<Search 
  placeholder="البحث في المنتجات..."
  onSearch={handleSearch}
  suggestions={searchSuggestions}
  debounce={300}
/>
```

### 📄 Pagination Component
```jsx
import { Pagination } from '../components/ui/Pagination'

<Pagination 
  currentPage={currentPage}
  totalPages={totalPages}
  onPageChange={handlePageChange}
  showInfo={true}
/>
```

### 🏷️ Badge Component
```jsx
import { Badge } from '../components/ui/Badge'

<Badge variant="success">نشط</Badge>
<Badge variant="warning">معلق</Badge>
<Badge variant="danger">محذوف</Badge>
```

## 📱 مكونات متجاوبة

### 📊 Dashboard Cards
```jsx
import { DashboardCard } from '../components/ui/DashboardCard'

<DashboardCard 
  title="إجمالي المبيعات"
  value="150,000 ريال"
  icon={<DollarSign />}
  trend="+12%"
  color="success"
/>
```

### 📈 Statistics Component
```jsx
import { Statistics } from '../components/ui/Statistics'

<Statistics 
  data={statsData}
  layout="grid"
  showTrends={true}
  period="monthly"
/>
```

## 🎭 مكونات التفاعل

### 🔔 Notification Component
```jsx
import { Notification } from '../components/common/Notification'

<Notification 
  type="success"
  message="تم حفظ البيانات بنجاح"
  autoClose={3000}
  position="top-right"
/>
```

### ⚠️ Confirmation Dialog
```jsx
import { ConfirmDialog } from '../components/common/ConfirmDialog'

<ConfirmDialog 
  isOpen={showConfirm}
  title="تأكيد الحذف"
  message="هل أنت متأكد من حذف هذا العنصر؟"
  onConfirm={handleConfirm}
  onCancel={handleCancel}
/>
```

## 🎨 نظام التصميم

### 🎨 Colors
```css
:root {
  --primary: #3b82f6;
  --secondary: #6b7280;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #06b6d4;
}
```

### 📏 Spacing
```css
.space-xs { margin: 0.25rem; }
.space-sm { margin: 0.5rem; }
.space-md { margin: 1rem; }
.space-lg { margin: 1.5rem; }
.space-xl { margin: 2rem; }
```

### 🔤 Typography
```css
.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
```

## 🔄 State Management

### 📦 Context Providers
```jsx
import { AppProvider } from '../contexts/AppContext'
import { AuthProvider } from '../contexts/AuthContext'
import { ThemeProvider } from '../contexts/ThemeContext'

<AppProvider>
  <AuthProvider>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </AuthProvider>
</AppProvider>
```

### 🎣 Custom Hooks
```jsx
import { useAuth } from '../hooks/useAuth'
import { useApi } from '../hooks/useApi'
import { useLocalStorage } from '../hooks/useLocalStorage'

// في المكون
const { user, login, logout } = useAuth()
const { data, loading, error } = useApi('/api/products')
const [theme, setTheme] = useLocalStorage('theme', 'light')
```

## 🧪 اختبار المكونات

### 🔬 Unit Tests
```jsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../Button'

test('renders button with text', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})

test('calls onClick when clicked', () => {
  const handleClick = jest.fn()
  render(<Button onClick={handleClick}>Click me</Button>)
  fireEvent.click(screen.getByText('Click me'))
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

## 📚 أفضل الممارسات

1. **استخدام TypeScript** للتحقق من الأنواع
2. **تقسيم المكونات** إلى مكونات صغيرة قابلة لإعادة الاستخدام
3. **استخدام Props Interface** لتوثيق الخصائص
4. **معالجة الأخطاء** في جميع المكونات
5. **الاختبار** لجميع المكونات المهمة
6. **الأداء** باستخدام React.memo و useMemo
7. **إمكانية الوصول** (Accessibility) في جميع المكونات
