/**
 * Roles and Permissions Management Page
 * صفحة إدارة الأدوار والأذونات
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Alert,
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Security as SecurityIcon,
  People as PeopleIcon
} from '@mui/icons-material';
import permissionService from '../services/permissionService';

const RolesPermissionsManagement = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState(''); // create, edit, permissions
  const [selectedRole, setSelectedRole] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rolesRes, permsRes] = await Promise.all([
        permissionService.getRoles(),
        permissionService.getPermissionsGrouped()
      ]);

      if (rolesRes.success) setRoles(rolesRes.data);
      if (permsRes.success) setPermissions(permsRes.data);
    } catch (err) {
      setError(err.message || 'فشل في تحميل البيانات');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateRole = () => {
    setSelectedRole(null);
    setDialogType('create');
    setDialogOpen(true);
  };

  const handleEditRole = async (roleId) => {
    try {
      const response = await permissionService.getRole(roleId);
      if (response.success) {
        setSelectedRole(response.data);
        setDialogType('edit');
        setDialogOpen(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleManagePermissions = async (roleId) => {
    try {
      const response = await permissionService.getRole(roleId);
      if (response.success) {
        setSelectedRole(response.data);
        setDialogType('permissions');
        setDialogOpen(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteRole = async (roleId) => {
    if (!window.confirm('هل أنت متأكد من حذف هذا الدور؟')) return;

    try {
      const response = await permissionService.deleteRole(roleId);
      if (response.success) {
        loadData();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const getPermissionCount = (role) => {
    if (!role.permissions) return 0;
    try {
      const perms = JSON.parse(role.permissions);
      return Array.isArray(perms) ? perms.length : 0;
    } catch {
      return 0;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">إدارة الأدوار والأذونات</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreateRole}
        >
          دور جديد
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab icon={<PeopleIcon />} label="الأدوار" />
          <Tab icon={<SecurityIcon />} label="الأذونات" />
        </Tabs>

        {activeTab === 0 && (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>الكود</TableCell>
                  <TableCell>الاسم</TableCell>
                  <TableCell>الوصف</TableCell>
                  <TableCell>عدد الأذونات</TableCell>
                  <TableCell>الحالة</TableCell>
                  <TableCell align="center">الإجراءات</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {roles.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography variant="body2" color="textSecondary">
                        لا توجد أدوار
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  roles.map((role) => (
                    <TableRow key={role.id} hover>
                      <TableCell>
                        <Chip
                          label={role.code}
                          size="small"
                          color={role.is_system ? 'primary' : 'default'}
                        />
                      </TableCell>
                      <TableCell>{role.name}</TableCell>
                      <TableCell>{role.description || '-'}</TableCell>
                      <TableCell>
                        <Chip
                          label={getPermissionCount(role)}
                          size="small"
                          color="info"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={role.is_active ? 'نشط' : 'معطل'}
                          size="small"
                          color={role.is_active ? 'success' : 'default'}
                        />
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          size="small"
                          onClick={() => handleManagePermissions(role.id)}
                          title="إدارة الأذونات"
                          color="primary"
                        >
                          <SecurityIcon fontSize="small" />
                        </IconButton>
                        
                        {!role.is_system && (
                          <>
                            <IconButton
                              size="small"
                              onClick={() => handleEditRole(role.id)}
                              title="تعديل"
                            >
                              <EditIcon fontSize="small" />
                            </IconButton>
                            
                            <IconButton
                              size="small"
                              onClick={() => handleDeleteRole(role.id)}
                              title="حذف"
                              color="error"
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {activeTab === 1 && (
          <Box sx={{ p: 3 }}>
            {Object.entries(permissions).map(([category, perms]) => (
              <Box key={category} sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  {category}
                </Typography>
                <Grid container spacing={1}>
                  {perms.map((perm) => (
                    <Grid item key={perm.code}>
                      <Chip
                        label={perm.name}
                        size="small"
                        variant="outlined"
                      />
                    </Grid>
                  ))}
                </Grid>
              </Box>
            ))}
          </Box>
        )}
      </Card>

      {/* Dialog for create/edit/permissions */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {dialogType === 'create' && 'دور جديد'}
          {dialogType === 'edit' && 'تعديل الدور'}
          {dialogType === 'permissions' && 'إدارة أذونات الدور'}
        </DialogTitle>
        <DialogContent>
          {selectedRole && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2">
                الدور: {selectedRole.name}
              </Typography>
              {/* Add form components here */}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>إغلاق</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default RolesPermissionsManagement;
