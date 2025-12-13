/**
 * صفحة إدارة المستخدمين
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/UserManagement.js
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePermissions } from '../contexts/PermissionContext';

const UserManagement = () => {
  const navigate = useNavigate();
  const { user: currentUser, hasPermission } = usePermissions();

  // ==================== State Management ====================
  
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // حالات النوافذ المنبثقة
  const [addUserDialogOpen, setAddUserDialogOpen] = useState(false);
  const [editUserDialogOpen, setEditUserDialogOpen] = useState(false);
  const [deleteUserDialogOpen, setDeleteUserDialogOpen] = useState(false);
  const [resetPasswordDialogOpen, setResetPasswordDialogOpen] = useState(false);
  const [permissionsDialogOpen, setPermissionsDialogOpen] = useState(false);
  
  // حالات القوائم المنسدلة
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  
  // حالات البحث والتصفية
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [warehouseFilter, setWarehouseFilter] = useState('');
  
  // بيانات النماذج
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    phone: '',
    full_name: '',
    role_id: '',
    warehouse_ids: [],
    is_active: true,
    password: '',
    confirm_password: ''
  });
  
  const [editUser, setEditUser] = useState({});
  const [newPassword, setNewPassword] = useState('');

  // ==================== Data Loading ====================

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // تحميل البيانات بشكل متوازي
      const [usersData, rolesData, warehousesData] = await Promise.allSettled([
        // userService.getAll(),
        // roleService.getAll(),
        // warehouseService.getAll()
        
        // بيانات تجريبية
        Promise.resolve([
          {
            id: 1,
            username: 'admin',
            email: 'admin@company.com',
            phone: '01234567890',
            full_name: 'مدير النظام',
            role: { id: 1, name: 'مدير النظام', permissions_count: 50 },
            warehouses: [{ id: 1, name: 'المخزن الرئيسي' }],
            is_active: true,
            last_login: new Date().toISOString(),
            created_at: '2024-01-01T00:00:00Z',
            login_count: 245
          },
          {
            id: 2,
            username: 'sales_manager',
            email: 'sales@company.com',
            phone: '01234567891',
            full_name: 'مدير المبيعات',
            role: { id: 2, name: 'مدير المبيعات', permissions_count: 25 },
            warehouses: [{ id: 1, name: 'المخزن الرئيسي' }, { id: 2, name: 'مخزن الفرع' }],
            is_active: true,
            last_login: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
            created_at: '2024-01-15T00:00:00Z',
            login_count: 156
          },
          {
            id: 3,
            username: 'warehouse_keeper',
            email: 'warehouse@company.com',
            phone: '01234567892',
            full_name: 'أمين المخزن',
            role: { id: 3, name: 'أمين مخزن', permissions_count: 15 },
            warehouses: [{ id: 1, name: 'المخزن الرئيسي' }],
            is_active: false,
            last_login: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
            created_at: '2024-02-01T00:00:00Z',
            login_count: 89
          }
        ]),
        Promise.resolve([
          { id: 1, name: 'مدير النظام', permissions_count: 50, users_count: 1 },
          { id: 2, name: 'مدير المبيعات', permissions_count: 25, users_count: 3 },
          { id: 3, name: 'أمين مخزن', permissions_count: 15, users_count: 5 },
          { id: 4, name: 'محاسب', permissions_count: 20, users_count: 2 },
          { id: 5, name: 'مهندس مبيعات', permissions_count: 12, users_count: 8 }
        ]),
        Promise.resolve([
          { id: 1, name: 'المخزن الرئيسي', location: 'القاهرة' },
          { id: 2, name: 'مخزن الفرع', location: 'الإسكندرية' },
          { id: 3, name: 'مخزن الجيزة', location: 'الجيزة' }
        ])
      ]);

      if (usersData.status === 'fulfilled') {
        setUsers(usersData.value);
      }

      if (rolesData.status === 'fulfilled') {
        setRoles(rolesData.value);
      }

      if (warehousesData.status === 'fulfilled') {
        setWarehouses(warehousesData.value);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ==================== Event Handlers ====================

  const handleAddUser = async () => {
    try {
      if (newUser.password !== newUser.confirm_password) {
        alert('كلمات المرور غير متطابقة');
        return;
      }

      // await userService.create(newUser);
      setAddUserDialogOpen(false);
      setNewUser({
        username: '',
        email: '',
        phone: '',
        full_name: '',
        role_id: '',
        warehouse_ids: [],
        is_active: true,
        password: '',
        confirm_password: ''
      });
      await loadData();
    } catch (error) {
      alert(`خطأ في إضافة المستخدم: ${error.message}`);
    }
  };

  const handleEditUser = async () => {
    try {
      // await userService.update(editUser.id, editUser);
      setEditUserDialogOpen(false);
      setEditUser({});
      await loadData();
    } catch (error) {
      alert(`خطأ في تحديث المستخدم: ${error.message}`);
    }
  };

  const handleDeleteUser = async () => {
    try {
      // await userService.delete(selectedUser.id);
      setDeleteUserDialogOpen(false);
      setSelectedUser(null);
      await loadData();
    } catch (error) {
      alert(`خطأ في حذف المستخدم: ${error.message}`);
    }
  };

  const handleResetPassword = async () => {
    try {
      // await userService.resetPassword(selectedUser.id, newPassword);
      setResetPasswordDialogOpen(false);
      setNewPassword('');
      setSelectedUser(null);
    } catch (error) {
      alert(`خطأ في إعادة تعيين كلمة المرور: ${error.message}`);
    }
  };

  const handleToggleUserStatus = async (userId, currentStatus) => {
    try {
      // await userService.toggleStatus(userId, !currentStatus);
      await loadData();
    } catch (error) {
      alert(`خطأ في تغيير حالة المستخدم: ${error.message}`);
    }
  };

  const handleMenuClick = (event, user) => {
    setAnchorEl(event.currentTarget);
    setSelectedUser(user);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedUser(null);
  };

  // ==================== Filter Functions ====================

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRole = !roleFilter || user.role.id.toString() === roleFilter;
    const matchesStatus = !statusFilter || 
                         (statusFilter === 'active' && user.is_active) ||
                         (statusFilter === 'inactive' && !user.is_active);
    
    const matchesWarehouse = !warehouseFilter || 
                           user.warehouses.some(w => w.id.toString() === warehouseFilter);

    return matchesSearch && matchesRole && matchesStatus && matchesWarehouse;
  });

  // ==================== Helper Functions ====================

  const getRoleColor = (roleName) => {
    const roleColors = {
      'مدير النظام': 'error',
      'مدير المبيعات': 'warning',
      'أمين مخزن': 'info',
      'محاسب': 'success',
      'مهندس مبيعات': 'primary'
    };
    return roleColors[roleName] || 'default';
  };

  const getLastLoginText = (lastLogin) => {
    if (!lastLogin) return 'لم يسجل دخول مطلقاً';
    
    const now = new Date();
    const loginDate = new Date(lastLogin);
    const diffInHours = Math.floor((now - loginDate) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'متصل الآن';
    if (diffInHours < 24) return `منذ ${diffInHours} ساعة`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `منذ ${diffInDays} يوم`;
    
    return loginDate.toLocaleDateString('ar-EG');
  };

  const isUserOnline = (lastLogin) => {
    if (!lastLogin) return false;
    const now = new Date();
    const loginDate = new Date(lastLogin);
    const diffInMinutes = Math.floor((now - loginDate) / (1000 * 60));
    return diffInMinutes < 30; // اعتبار المستخدم متصل إذا سجل دخول خلال آخر 30 دقيقة
  };

  // ==================== Render Functions ====================

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          جاري تحميل المستخدمين...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        خطأ في تحميل المستخدمين: {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            إدارة المستخدمين
          </Typography>
          <Typography variant="body1" color="text.secondary">
            إدارة حسابات المستخدمين والصلاحيات
          </Typography>
        </Box>
        
        <Box display="flex" gap={1}>
          <ProtectedButton
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={() => {/* تصدير المستخدمين */}}
          >
            تصدير
          </ProtectedButton>
          
          <ProtectedButton
            variant="outlined"
            startIcon={<UploadIcon />}
            onClick={() => {/* استيراد المستخدمين */}}
          >
            استيراد
          </ProtectedButton>
          
          <ProtectedButton
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setAddUserDialogOpen(true)}
            requiredPermission="add_user"
          >
            إضافة مستخدم
          </ProtectedButton>
        </Box>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <PersonIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{users.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    إجمالي المستخدمين
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <CheckCircleIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {users.filter(u => u.is_active).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    المستخدمين النشطين
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <Badge color="success" variant="dot">
                    <PersonIcon />
                  </Badge>
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {users.filter(u => isUserOnline(u.last_login)).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    متصلين الآن
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <SecurityIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{roles.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    الأدوار المتاحة
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                size="small"
                placeholder="البحث في المستخدمين..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
                }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>الدور</InputLabel>
                <Select
                  value={roleFilter}
                  onChange={(e) => setRoleFilter(e.target.value)}
                  label="الدور"
                >
                  <MenuItem value="">الكل</MenuItem>
                  {roles.map(role => (
                    <MenuItem key={role.id} value={role.id.toString()}>
                      {role.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>الحالة</InputLabel>
                <Select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  label="الحالة"
                >
                  <MenuItem value="">الكل</MenuItem>
                  <MenuItem value="active">نشط</MenuItem>
                  <MenuItem value="inactive">غير نشط</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>المخزن</InputLabel>
                <Select
                  value={warehouseFilter}
                  onChange={(e) => setWarehouseFilter(e.target.value)}
                  label="المخزن"
                >
                  <MenuItem value="">الكل</MenuItem>
                  {warehouses.map(warehouse => (
                    <MenuItem key={warehouse.id} value={warehouse.id.toString()}>
                      {warehouse.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Box display="flex" gap={1}>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<FilterListIcon />}
                  onClick={() => {
                    setSearchTerm('');
                    setRoleFilter('');
                    setStatusFilter('');
                    setWarehouseFilter('');
                  }}
                >
                  مسح الفلاتر
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>المستخدم</TableCell>
                <TableCell>الدور</TableCell>
                <TableCell>المخازن</TableCell>
                <TableCell>الحالة</TableCell>
                <TableCell>آخر تسجيل دخول</TableCell>
                <TableCell>عدد مرات الدخول</TableCell>
                <TableCell>الإجراءات</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredUsers.map((user) => (
                <TableRow key={user.id} hover>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <Badge
                        color="success"
                        variant="dot"
                        invisible={!isUserOnline(user.last_login)}
                      >
                        <Avatar sx={{ mr: 2 }}>
                          {user.full_name.charAt(0)}
                        </Avatar>
                      </Badge>
                      <Box>
                        <Typography variant="body1" fontWeight="bold">
                          {user.full_name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          @{user.username}
                        </Typography>
                        <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                          <EmailIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                          <Typography variant="caption">{user.email}</Typography>
                        </Box>
                        {user.phone && (
                          <Box display="flex" alignItems="center" gap={1}>
                            <PhoneIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
                            <Typography variant="caption">{user.phone}</Typography>
                          </Box>
                        )}
                      </Box>
                    </Box>
                  </TableCell>
                  
                  <TableCell>
                    <Chip
                      label={user.role.name}
                      color={getRoleColor(user.role.name)}
                      size="small"
                      icon={user.role.name === 'مدير النظام' ? <AdminIcon /> : <SecurityIcon />}
                    />
                    <Typography variant="caption" display="block" sx={{ mt: 0.5 }}>
                      {user.role.permissions_count} صلاحية
                    </Typography>
                  </TableCell>
                  
                  <TableCell>
                    <Box>
                      {user.warehouses.slice(0, 2).map((warehouse, index) => (
                        <Chip
                          key={warehouse.id}
                          label={warehouse.name}
                          size="small"
                          variant="outlined"
                          sx={{ mr: 0.5, mb: 0.5 }}
                        />
                      ))}
                      {user.warehouses.length > 2 && (
                        <Chip
                          label={`+${user.warehouses.length - 2}`}
                          size="small"
                          variant="outlined"
                          color="primary"
                        />
                      )}
                    </Box>
                  </TableCell>
                  
                  <TableCell>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Chip
                        label={user.is_active ? 'نشط' : 'غير نشط'}
                        color={user.is_active ? 'success' : 'error'}
                        size="small"
                      />
                      {isUserOnline(user.last_login) && (
                        <Chip
                          label="متصل"
                          color="info"
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </TableCell>
                  
                  <TableCell>
                    <Typography variant="body2">
                      {getLastLoginText(user.last_login)}
                    </Typography>
                  </TableCell>
                  
                  <TableCell>
                    <Typography variant="body2">
                      {user.login_count || 0}
                    </Typography>
                  </TableCell>
                  
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <ProtectedComponent requiredPermission="edit_user">
                        <Tooltip title="تعديل">
                          <IconButton
                            size="small"
                            onClick={() => {
                              setEditUser(user);
                              setEditUserDialogOpen(true);
                            }}
                          >
                            <EditIcon />
                          </IconButton>
                        </Tooltip>
                      </ProtectedComponent>
                      
                      <ProtectedComponent requiredPermission="manage_user_status">
                        <Tooltip title={user.is_active ? 'إلغاء التفعيل' : 'تفعيل'}>
                          <IconButton
                            size="small"
                            onClick={() => handleToggleUserStatus(user.id, user.is_active)}
                            color={user.is_active ? 'error' : 'success'}
                          >
                            {user.is_active ? <BlockIcon /> : <CheckCircleIcon />}
                          </IconButton>
                        </Tooltip>
                      </ProtectedComponent>
                      
                      <IconButton
                        size="small"
                        onClick={(e) => handleMenuClick(e, user)}
                      >
                        <MoreVertIcon />
                      </IconButton>
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <ProtectedComponent requiredPermission="view_user_details">
          <MenuItem onClick={() => {
            navigate(`/settings/users/${selectedUser?.id}`);
            handleMenuClose();
          }}>
            <ListItemIcon><VisibilityIcon /></ListItemIcon>
            <ListItemText>عرض التفاصيل</ListItemText>
          </MenuItem>
        </ProtectedComponent>
        
        <ProtectedComponent requiredPermission="manage_user_permissions">
          <MenuItem onClick={() => {
            setPermissionsDialogOpen(true);
            handleMenuClose();
          }}>
            <ListItemIcon><SecurityIcon /></ListItemIcon>
            <ListItemText>إدارة الصلاحيات</ListItemText>
          </MenuItem>
        </ProtectedComponent>
        
        <ProtectedComponent requiredPermission="reset_user_password">
          <MenuItem onClick={() => {
            setResetPasswordDialogOpen(true);
            handleMenuClose();
          }}>
            <ListItemIcon><VpnKeyIcon /></ListItemIcon>
            <ListItemText>إعادة تعيين كلمة المرور</ListItemText>
          </MenuItem>
        </ProtectedComponent>
        
        <Divider />
        
        <ProtectedComponent requiredPermission="view_user_history">
          <MenuItem onClick={() => {
            navigate(`/settings/users/${selectedUser?.id}/history`);
            handleMenuClose();
          }}>
            <ListItemIcon><HistoryIcon /></ListItemIcon>
            <ListItemText>سجل النشاط</ListItemText>
          </MenuItem>
        </ProtectedComponent>
        
        <ProtectedComponent requiredPermission="delete_user">
          <MenuItem 
            onClick={() => {
              setDeleteUserDialogOpen(true);
              handleMenuClose();
            }}
            sx={{ color: 'error.main' }}
          >
            <ListItemIcon><DeleteIcon color="error" /></ListItemIcon>
            <ListItemText>حذف المستخدم</ListItemText>
          </MenuItem>
        </ProtectedComponent>
      </Menu>

      {/* Add User Dialog */}
      <Dialog open={addUserDialogOpen} onClose={() => setAddUserDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>إضافة مستخدم جديد</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="اسم المستخدم"
                value={newUser.username}
                onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الاسم الكامل"
                value={newUser.full_name}
                onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="البريد الإلكتروني"
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="رقم الهاتف"
                value={newUser.phone}
                onChange={(e) => setNewUser({ ...newUser, phone: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required>
                <InputLabel>الدور</InputLabel>
                <Select
                  value={newUser.role_id}
                  onChange={(e) => setNewUser({ ...newUser, role_id: e.target.value })}
                  label="الدور"
                >
                  {roles.map(role => (
                    <MenuItem key={role.id} value={role.id}>
                      {role.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>المخازن</InputLabel>
                <Select
                  multiple
                  value={newUser.warehouse_ids}
                  onChange={(e) => setNewUser({ ...newUser, warehouse_ids: e.target.value })}
                  label="المخازن"
                  renderValue={(selected) => 
                    warehouses
                      .filter(w => selected.includes(w.id))
                      .map(w => w.name)
                      .join(', ')
                  }
                >
                  {warehouses.map(warehouse => (
                    <MenuItem key={warehouse.id} value={warehouse.id}>
                      {warehouse.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="كلمة المرور"
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="تأكيد كلمة المرور"
                type="password"
                value={newUser.confirm_password}
                onChange={(e) => setNewUser({ ...newUser, confirm_password: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={newUser.is_active}
                    onChange={(e) => setNewUser({ ...newUser, is_active: e.target.checked })}
                  />
                }
                label="تفعيل المستخدم"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddUserDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleAddUser} variant="contained">إضافة</Button>
        </DialogActions>
      </Dialog>

      {/* Edit User Dialog */}
      <Dialog open={editUserDialogOpen} onClose={() => setEditUserDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>تعديل المستخدم</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="اسم المستخدم"
                value={editUser.username || ''}
                onChange={(e) => setEditUser({ ...editUser, username: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الاسم الكامل"
                value={editUser.full_name || ''}
                onChange={(e) => setEditUser({ ...editUser, full_name: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="البريد الإلكتروني"
                type="email"
                value={editUser.email || ''}
                onChange={(e) => setEditUser({ ...editUser, email: e.target.value })}
                required
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="رقم الهاتف"
                value={editUser.phone || ''}
                onChange={(e) => setEditUser({ ...editUser, phone: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={editUser.is_active || false}
                    onChange={(e) => setEditUser({ ...editUser, is_active: e.target.checked })}
                  />
                }
                label="تفعيل المستخدم"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditUserDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleEditUser} variant="contained">حفظ</Button>
        </DialogActions>
      </Dialog>

      {/* Reset Password Dialog */}
      <Dialog open={resetPasswordDialogOpen} onClose={() => setResetPasswordDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>إعادة تعيين كلمة المرور</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            إعادة تعيين كلمة المرور للمستخدم: {selectedUser?.full_name}
          </Typography>
          <TextField
            fullWidth
            label="كلمة المرور الجديدة"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResetPasswordDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleResetPassword} variant="contained" color="warning">
            إعادة تعيين
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete User Dialog */}
      <Dialog open={deleteUserDialogOpen} onClose={() => setDeleteUserDialogOpen(false)}>
        <DialogTitle>تأكيد الحذف</DialogTitle>
        <DialogContent>
          <Typography>
            هل أنت متأكد من حذف المستخدم "{selectedUser?.full_name}"؟
            هذا الإجراء لا يمكن التراجع عنه.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteUserDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleDeleteUser} color="error" variant="contained">حذف</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserManagement;

