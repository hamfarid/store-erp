# تحليل تفصيلي لمكونات React - Gaara ERP v12

## نظرة عامة
تحليل تفصيلي لمكونات React المقترحة لنظام Gaara ERP v12 مع الكود المصدري الأولي.

## 1. المكونات الأساسية (Core Components)

### 1.1 `AppLayout.jsx`
```jsx
// src/components/core/AppLayout.jsx
import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';
import { Box, Grid } from '@mui/material';

const AppLayout = ({ children }) => {
  return (
    <Box sx={{ display: 'flex' }}>
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Header />
        <Box sx={{ mt: 8 }}>
          {children}
        </Box>
        <Footer />
      </Box>
    </Box>
  );
};

export default AppLayout;
```

### 1.2 `DataTable.jsx`
```jsx
// src/components/data/DataTable.jsx
import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Box, CircularProgress } from '@mui/material';

const DataTable = ({ rows, columns, loading, ...props }) => {
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 25, 50]}
        checkboxSelection
        disableSelectionOnClick
        {...props}
      />
    </Box>
  );
};

export default DataTable;
```

## 2. مكونات النماذج (Form Components)

### 2.1 `TextInput.jsx`
```jsx
// src/components/forms/TextInput.jsx
import React from 'react';
import { TextField } from '@mui/material';
import { useController } from 'react-hook-form';

const TextInput = ({ control, name, label, ...props }) => {
  const { field, fieldState: { error } } = useController({
    name,
    control,
    defaultValue: ''
  });

  return (
    <TextField
      {...field}
      label={label}
      error={!!error}
      helperText={error?.message}
      fullWidth
      margin="normal"
      {...props}
    />
  );
};

export default TextInput;
```

### 2.2 `DatePicker.jsx`
```jsx
// src/components/forms/DatePicker.jsx
import React from 'react';
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker as MuiDatePicker } from '@mui/x-date-pickers/DatePicker';
import { useController } from 'react-hook-form';

const DatePicker = ({ control, name, label, ...props }) => {
  const { field, fieldState: { error } } = useController({
    name,
    control,
    defaultValue: null
  });

  return (
    <LocalizationProvider dateAdapter={AdapterMoment}>
      <MuiDatePicker
        {...field}
        label={label}
        renderInput={(params) => (
          <TextField
            {...params}
            fullWidth
            margin="normal"
            error={!!error}
            helperText={error?.message}
          />
        )}
        {...props}
      />
    </LocalizationProvider>
  );
};

export default DatePicker;
```

## 3. مكونات لوحة التحكم (Dashboard Components)

### 3.1 `StatCard.jsx`
```jsx
// src/components/dashboard/StatCard.jsx
import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const StatCard = ({ title, value, icon, color = 'primary.main' }) => {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ flexGrow: 1 }}>
            <Typography color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
          </Box>
          <Box sx={{ color }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatCard;
```

### 3.2 `ChartWidget.jsx`
```jsx
// src/components/dashboard/ChartWidget.jsx
import React from 'react';
import { Card, CardContent, CardHeader, Box } from '@mui/material';
import { Line } from 'react-chartjs-2';

const ChartWidget = ({ title, data, options }) => {
  return (
    <Card>
      <CardHeader title={title} />
      <CardContent>
        <Box sx={{ height: 300, position: 'relative' }}>
          <Line data={data} options={options} />
        </Box>
      </CardContent>
    </Card>
  );
};

export default ChartWidget;
```

## 4. مكونات الوحدات التجارية (Business Module Components)

### 4.1 `ChartOfAccounts.jsx` (المحاسبة)
```jsx
// src/components/accounting/ChartOfAccounts.jsx
import React, { useState, useEffect } from 'react';
import { TreeView, TreeItem } from '@mui/lab';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { api } from '@/services';

const ChartOfAccounts = () => {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      const response = await api.get('/accounting/accounts/tree/');
      setAccounts(response.data);
    };
    fetchAccounts();
  }, []);

  const renderTree = (nodes) => (
    <TreeItem key={nodes.id} nodeId={String(nodes.id)} label={`${nodes.code} - ${nodes.name}`}>
      {Array.isArray(nodes.children) ? nodes.children.map((node) => renderTree(node)) : null}
    </TreeItem>
  );

  return (
    <TreeView
      defaultCollapseIcon={<ExpandMoreIcon />}
      defaultExpandIcon={<ChevronRightIcon />}
    >
      {accounts.map((account) => renderTree(account))}
    </TreeView>
  );
};

export default ChartOfAccounts;
```

### 4.2 `ProductCatalog.jsx` (المخزون)
```jsx
// src/components/inventory/ProductCatalog.jsx
import React from 'react';
import { useQuery } from 'react-query';
import { Grid, Card, CardMedia, CardContent, Typography } from '@mui/material';
import { api } from '@/services';

const fetchProducts = async () => {
  const { data } = await api.get('/inventory/products/');
  return data.results;
};

const ProductCatalog = () => {
  const { data: products, isLoading } = useQuery('products', fetchProducts);

  if (isLoading) return <p>Loading...</p>;

  return (
    <Grid container spacing={3}>
      {products.map((product) => (
        <Grid item key={product.id} xs={12} sm={6} md={4}>
          <Card>
            <CardMedia
              component="img"
              height="140"
              image={product.image || '/placeholder.png'}
              alt={product.name}
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                {product.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {product.description}
              </Typography>
              <Typography variant="h6" color="primary">
                {product.unit_price} SAR
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default ProductCatalog;
```

## 5. مثال على صفحة (Page Example)

### 5.1 `Dashboard.jsx`
```jsx
// src/pages/Dashboard.jsx
import React from 'react';
import { Grid, Typography } from '@mui/material';
import StatCard from '@/components/dashboard/StatCard';
import ChartWidget from '@/components/dashboard/ChartWidget';
import SalesIcon from '@mui/icons-material/MonetizationOn';
import CustomerIcon from '@mui/icons-material/People';

const Dashboard = () => {
  // Dummy data for charts
  const salesData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Sales',
        data: [12000, 19000, 15000, 21000, 18000, 25000],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard title="Total Sales" value="150,000 SAR" icon={<SalesIcon />} />
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard title="New Customers" value="120" icon={<CustomerIcon />} color="success.main" />
      </Grid>
      {/* ... other stat cards ... */}

      <Grid item xs={12} md={8}>
        <ChartWidget title="Sales Over Time" data={salesData} />
      </Grid>
      <Grid item xs={12} md={4}>
        {/* ... another widget ... */}
      </Grid>
    </Grid>
  );
};

export default Dashboard;
```

---

**تاريخ التوثيق**: نوفمبر 2025  
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition  
**حالة التوثيق**: مقترح للتطوير المستقبلي
