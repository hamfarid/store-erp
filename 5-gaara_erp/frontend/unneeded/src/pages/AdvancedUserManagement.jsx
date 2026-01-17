// /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/AdvancedUserManagement.js

import React, { useState, useEffect } from 'react';
import { usePermissions } from '../contexts/PermissionContext.jsx';

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`user-tabpanel-${index}`}
      aria-labelledby={`user-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const AdvancedUserManagement = () => {
  const { hasPermission } = usePermissions();
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedUser, setSelectedUser] = useState(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  // حوارات
  const [dialogs, setDialogs] = useState({
    addUser: false,
    editUser: false,
    deleteUser: false,
    addGroup: false,
    editGroup: false,
    deleteGroup: false,
    userDetails: false,
    resetPassword: false,
    bulkActions: false
  });

  // قائمة المستخدمين التجريبية
  const [sampleUsers] = useState([
    {
      id: 1,
      firstName: 'أحمد',
      lastName: 'محمد',
      email: 'ahmed@company.com',
      phone: '+966501234567',
      role: 'مدير',
      department: 'المبيعات',
      status: 'active',
      lastLogin: '2024-01-15 10:30',
      createdAt: '2024-01-01',
      avatar: null,
      permissions: ['sales_read', 'sales_write', 'inventory_read'],
      groups: ['مديري المبيعات', 'المستخدمين الأساسيين']
    },
    {
      id: 2,
      firstName: 'فاطمة',
      lastName: 'علي',
      email: 'fatima@company.com',
      phone: '+966507654321',
      role: 'محاسب',
      department: 'المحاسبة',
      status: 'active',
      lastLogin: '2024-01-14 16:45',
      createdAt: '2024-01-02',
      avatar: null,
      permissions: ['accounting_read', 'accounting_write', 'reports_read'],
      groups: ['المحاسبين', 'المستخدمين الأساسيين']
    },
    {
      id: 3,
      firstName: 'محمد',
      lastName: 'خالد',
      email: 'mohammed@company.com',
      phone: '+966509876543',
      role: 'مشرف مخزن',
      department: 'المخازن',
      status: 'inactive',
      lastLogin: '2024-01-10 09:15',
      createdAt: '2024-01-03',
      avatar: null,
      permissions: ['inventory_read', 'inventory_write', 'warehouse_manage'],
      groups: ['مشرفي المخازن']
    }
  ]);

  // مجموعات المستخدمين التجريبية
  const [sampleGroups] = useState([
    {
      id: 1,
      name: 'المستخدمين الأساسيين',
      description: 'مجموعة المستخدمين الأساسيين مع الصلاحيات الأساسية',
      permissions: ['dashboard_read', 'profile_read', 'profile_write'],
      userCount: 15,
      createdAt: '2024-01-01',
      color: '#1976d2'
    },
    {
      id: 2,
      name: 'مديري المبيعات',
      description: 'مديري المبيعات مع صلاحيات إدارة المبيعات والعملاء',
      permissions: ['sales_read', 'sales_write', 'customers_read', 'customers_write'],
      userCount: 5,
      createdAt: '2024-01-01',
      color: '#388e3c'
    },
    {
      id: 3,
      name: 'المحاسبين',
      description: 'المحاسبين مع صلاحيات إدارة الحسابات والتقارير المالية',
      permissions: ['accounting_read', 'accounting_write', 'reports_read', 'reports_write'],
      userCount: 3,
      createdAt: '2024-01-01',
      color: '#f57c00'
    },
    {
      id: 4,
      name: 'مشرفي المخازن',
      description: 'مشرفي المخازن مع صلاحيات إدارة المخزون والمخازن',
      permissions: ['inventory_read', 'inventory_write', 'warehouse_manage'],
      userCount: 8,
      createdAt: '2024-01-01',
      color: '#7b1fa2'
    }
  ]);

  // بيانات المستخدم الجديد
  const [newUser, setNewUser] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    role: '',
    department: '',
    password: '',
    confirmPassword: '',
    groups: [],
    permissions: [],
    status: 'active'
  });

  // بيانات المجموعة الجديدة
  const [newGroup, setNewGroup] = useState({
    name: '',
    description: '',
    permissions: [],
    color: '#1976d2'
  });

  useEffect(() => {
    loadUsers();
    loadGroups();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      // هنا يتم تحميل المستخدمين من الخادم
      setUsers(sampleUsers);
    } catch (error) {
      showSnackbar('خطأ في تحميل المستخدمين', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadGroups = async () => {
    try {
      setLoading(true);
      // هنا يتم تحميل المجموعات من الخادم
      setGroups(sampleGroups);
    } catch (error) {
      showSnackbar('خطأ في تحميل المجموعات', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showSnackbar = (message, severity = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.role.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = filterStatus === 'all' || user.status === filterStatus;
    
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'inactive':
        return 'default';
      case 'blocked':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active':
        return 'نشط';
      case 'inactive':
        return 'غير نشط';
      case 'blocked':
        return 'محظور';
      default:
        return status;
    }
  };

  const handleAddUser = async () => {
    try {
      setLoading(true);
      // هنا يتم إضافة المستخدم الجديد
      const newUserData = {
        ...newUser,
        id: users.length + 1,
        createdAt: new Date().toISOString().split('T')[0],
        lastLogin: null,
        avatar: null
      };
      setUsers(prev => [...prev, newUserData]);
      setDialogs(prev => ({ ...prev, addUser: false }));
      setNewUser({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        role: '',
        department: '',
        password: '',
        confirmPassword: '',
        groups: [],
        permissions: [],
        status: 'active'
      });
      showSnackbar('تم إضافة المستخدم بنجاح');
    } catch (error) {
      showSnackbar('خطأ في إضافة المستخدم', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId) => {
    try {
      setLoading(true);
      // هنا يتم حذف المستخدم
      setUsers(prev => prev.filter(user => user.id !== userId));
      setDialogs(prev => ({ ...prev, deleteUser: false }));
      showSnackbar('تم حذف المستخدم بنجاح');
    } catch (error) {
      showSnackbar('خطأ في حذف المستخدم', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddGroup = async () => {
    try {
      setLoading(true);
      // هنا يتم إضافة المجموعة الجديدة
      const newGroupData = {
        ...newGroup,
        id: groups.length + 1,
        userCount: 0,
        createdAt: new Date().toISOString().split('T')[0]
      };
      setGroups(prev => [...prev, newGroupData]);
      setDialogs(prev => ({ ...prev, addGroup: false }));
      setNewGroup({
        name: '',
        description: '',
        permissions: [],
        color: '#1976d2'
      });
      showSnackbar('تم إضافة المجموعة بنجاح');
    } catch (error) {
      showSnackbar('خطأ في إضافة المجموعة', 'error');
    } finally {
      setLoading(false);
    }
  };

  // التحقق من الصلاحيات
  if (!hasPermission('users', 'read')) {
    return (
      <Container>
        <Alert severity="error">
          ليس لديك صلاحية للوصول إلى إدارة المستخدمين
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          <PersonIcon sx={{ mr: 2, verticalAlign: 'middle' }} />
          إدارة المستخدمين المتقدمة
        </Typography>
        <Typography variant="body1" color="text.secondary">
          إدارة شاملة للمستخدمين والمجموعات والصلاحيات
        </Typography>
      </Box>

      {/* إحصائيات سريعة */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
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
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <CheckCircleIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {users.filter(u => u.status === 'active').length}
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
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <GroupIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">{groups.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    المجموعات
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <SecurityIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6">
                    {users.filter(u => u.lastLogin && 
                      new Date(u.lastLogin) > new Date(Date.now() - 24*60*60*1000)
                    ).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    نشط اليوم
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="المستخدمين" icon={<PersonIcon />} />
          <Tab label="المجموعات" icon={<GroupIcon />} />
          <Tab label="الصلاحيات" icon={<SecurityIcon />} />
          <Tab label="سجل النشاط" icon={<HistoryIcon />} />
        </Tabs>

        {/* تبويب المستخدمين */}
        <TabPanel value={activeTab} index={0}>
          {/* شريط الأدوات */}
          <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
            <TextField
              size="small"
              placeholder="البحث في المستخدمين..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
              }}
              sx={{ minWidth: 250 }}
            />
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>الحالة</InputLabel>
              <Select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <MenuItem value="all">الكل</MenuItem>
                <MenuItem value="active">نشط</MenuItem>
                <MenuItem value="inactive">غير نشط</MenuItem>
                <MenuItem value="blocked">محظور</MenuItem>
              </Select>
            </FormControl>
            <Box sx={{ flexGrow: 1 }} />
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={() => {/* تصدير البيانات */}}
            >
              تصدير
            </Button>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={loadUsers}
            >
              تحديث
            </Button>
            {hasPermission('users', 'create') && (
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setDialogs(prev => ({ ...prev, addUser: true }))}
              >
                إضافة مستخدم
              </Button>
            )}
          </Box>

          {/* جدول المستخدمين */}
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>المستخدم</TableCell>
                  <TableCell>البريد الإلكتروني</TableCell>
                  <TableCell>الدور</TableCell>
                  <TableCell>القسم</TableCell>
                  <TableCell>الحالة</TableCell>
                  <TableCell>آخر دخول</TableCell>
                  <TableCell align="center">الإجراءات</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredUsers
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((user) => (
                    <TableRow key={user.id} hover>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Avatar sx={{ mr: 2 }}>
                            {user.firstName.charAt(0)}
                          </Avatar>
                          <Box>
                            <Typography variant="body2" fontWeight="medium">
                              {user.firstName} {user.lastName}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {user.phone}
                            </Typography>
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>
                        <Chip label={user.role} size="small" />
                      </TableCell>
                      <TableCell>{user.department}</TableCell>
                      <TableCell>
                        <Chip
                          label={getStatusText(user.status)}
                          color={getStatusColor(user.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {user.lastLogin ? (
                          <Typography variant="body2">
                            {new Date(user.lastLogin).toLocaleDateString('ar-SA')}
                          </Typography>
                        ) : (
                          <Typography variant="body2" color="text.secondary">
                            لم يسجل دخول
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip title="عرض التفاصيل">
                          <IconButton
                            size="small"
                            onClick={() => {
                              setSelectedUser(user);
                              setDialogs(prev => ({ ...prev, userDetails: true }));
                            }}
                          >
                            <VisibilityIcon />
                          </IconButton>
                        </Tooltip>
                        {hasPermission('users', 'update') && (
                          <Tooltip title="تعديل">
                            <IconButton
                              size="small"
                              onClick={() => {
                                setSelectedUser(user);
                                setDialogs(prev => ({ ...prev, editUser: true }));
                              }}
                            >
                              <EditIcon />
                            </IconButton>
                          </Tooltip>
                        )}
                        {hasPermission('users', 'delete') && (
                          <Tooltip title="حذف">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => {
                                setSelectedUser(user);
                                setDialogs(prev => ({ ...prev, deleteUser: true }));
                              }}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>

          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={filteredUsers.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage="عدد الصفوف في الصفحة:"
            labelDisplayedRows={({ from, to, count }) => 
              `${from}-${to} من ${count !== -1 ? count : `أكثر من ${to}`}`
            }
          />
        </TabPanel>

        {/* تبويب المجموعات */}
        <TabPanel value={activeTab} index={1}>
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">
              مجموعات المستخدمين ({groups.length})
            </Typography>
            {hasPermission('groups', 'create') && (
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setDialogs(prev => ({ ...prev, addGroup: true }))}
              >
                إضافة مجموعة
              </Button>
            )}
          </Box>

          <Grid container spacing={3}>
            {groups.map((group) => (
              <Grid item xs={12} md={6} lg={4} key={group.id}>
                <Card>
                  <CardHeader
                    avatar={
                      <Avatar sx={{ bgcolor: group.color }}>
                        <GroupIcon />
                      </Avatar>
                    }
                    title={group.name}
                    subheader={`${group.userCount} مستخدم`}
                    action={
                      <IconButton>
                        <MoreVertIcon />
                      </IconButton>
                    }
                  />
                  <CardContent>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {group.description}
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="caption" color="text.secondary">
                        الصلاحيات ({group.permissions.length})
                      </Typography>
                      <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {group.permissions.slice(0, 3).map((permission, index) => (
                          <Chip
                            key={index}
                            label={permission}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                        {group.permissions.length > 3 && (
                          <Chip
                            label={`+${group.permissions.length - 3}`}
                            size="small"
                            variant="outlined"
                          />
                        )}
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* باقي التبويبات... */}
      </Paper>

      {/* حوار إضافة مستخدم */}
      <Dialog
        open={dialogs.addUser}
        onClose={() => setDialogs(prev => ({ ...prev, addUser: false }))}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>إضافة مستخدم جديد</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الاسم الأول"
                value={newUser.firstName}
                onChange={(e) => setNewUser(prev => ({ ...prev, firstName: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الاسم الأخير"
                value={newUser.lastName}
                onChange={(e) => setNewUser(prev => ({ ...prev, lastName: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="البريد الإلكتروني"
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser(prev => ({ ...prev, email: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="رقم الهاتف"
                value={newUser.phone}
                onChange={(e) => setNewUser(prev => ({ ...prev, phone: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="الدور"
                value={newUser.role}
                onChange={(e) => setNewUser(prev => ({ ...prev, role: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="القسم"
                value={newUser.department}
                onChange={(e) => setNewUser(prev => ({ ...prev, department: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="كلمة المرور"
                type="password"
                value={newUser.password}
                onChange={(e) => setNewUser(prev => ({ ...prev, password: e.target.value }))}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="تأكيد كلمة المرور"
                type="password"
                value={newUser.confirmPassword}
                onChange={(e) => setNewUser(prev => ({ ...prev, confirmPassword: e.target.value }))}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogs(prev => ({ ...prev, addUser: false }))}>
            إلغاء
          </Button>
          <Button onClick={handleAddUser} variant="contained" disabled={loading}>
            إضافة
          </Button>
        </DialogActions>
      </Dialog>

      {/* حوار حذف مستخدم */}
      <Dialog
        open={dialogs.deleteUser}
        onClose={() => setDialogs(prev => ({ ...prev, deleteUser: false }))}
      >
        <DialogTitle>تأكيد الحذف</DialogTitle>
        <DialogContent>
          <Typography>
            هل أنت متأكد من حذف المستخدم "{selectedUser?.firstName} {selectedUser?.lastName}"؟
            هذا الإجراء لا يمكن التراجع عنه.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogs(prev => ({ ...prev, deleteUser: false }))}>
            إلغاء
          </Button>
          <Button 
            onClick={() => handleDeleteUser(selectedUser?.id)} 
            color="error" 
            variant="contained"
            disabled={loading}
          >
            حذف
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar للإشعارات */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AdvancedUserManagement;

