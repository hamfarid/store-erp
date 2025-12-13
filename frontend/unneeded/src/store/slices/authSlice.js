// Authentication Slice
// شريحة المصادقة

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import authAPI from '../../services/authAPI';

// Initial state
const initialState = {
  user: null,
  token: null,
  refreshToken: null,
  permissions: [],
  isAuthenticated: false,
  isLoading: false,
  error: null,
  loginAttempts: 0,
  lastLoginTime: null,
  sessionExpiry: null,
  mfaRequired: false,
  mfaToken: null
};

// Async thunks
export const loginUser = createAsyncThunk(
  'auth/loginUser',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await authAPI.login(credentials);
      
      // Store tokens securely
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      
      return {
        user: response.data.user,
        token: response.data.access_token,
        refreshToken: response.data.refresh_token,
        permissions: response.data.permissions || [],
        sessionExpiry: response.data.expires_at
      };
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في تسجيل الدخول'
      );
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/registerUser',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await authAPI.register(userData);
      return {
        user: response.data.user,
        token: response.data.access_token,
        refreshToken: response.data.refresh_token,
        permissions: response.data.permissions || []
      };
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في إنشاء الحساب'
      );
    }
  }
);

export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { getState, rejectWithValue }) => {
    try {
      const { auth } = getState();
      const response = await authAPI.refreshToken(auth.refreshToken);
      
      localStorage.setItem('accessToken', response.data.access_token);
      
      return {
        token: response.data.access_token,
        sessionExpiry: response.data.expires_at
      };
    } catch (error) {
      return rejectWithValue('فشل في تجديد الجلسة');
    }
  }
);

export const logoutUser = createAsyncThunk(
  'auth/logoutUser',
  async (_, { getState }) => {
    try {
      const { auth } = getState();
      await authAPI.logout(auth.token);
    } catch (error) {
      // Continue with logout even if API call fails
      console.error('Logout API error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }
);

export const updateProfile = createAsyncThunk(
  'auth/updateProfile',
  async (profileData, { rejectWithValue }) => {
    try {
      const response = await authAPI.updateProfile(profileData);
      return response.data.user;
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في تحديث الملف الشخصي'
      );
    }
  }
);

export const changePassword = createAsyncThunk(
  'auth/changePassword',
  async (passwordData, { rejectWithValue }) => {
    try {
      await authAPI.changePassword(passwordData);
      return 'تم تغيير كلمة المرور بنجاح';
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في تغيير كلمة المرور'
      );
    }
  }
);

export const verifyMFA = createAsyncThunk(
  'auth/verifyMFA',
  async ({ token, code }, { rejectWithValue }) => {
    try {
      const response = await authAPI.verifyMFA(token, code);
      
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      
      return {
        user: response.data.user,
        token: response.data.access_token,
        refreshToken: response.data.refresh_token,
        permissions: response.data.permissions || []
      };
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'رمز التحقق غير صحيح'
      );
    }
  }
);

export const requestPasswordReset = createAsyncThunk(
  'auth/requestPasswordReset',
  async (email, { rejectWithValue }) => {
    try {
      await authAPI.requestPasswordReset(email);
      return 'تم إرسال رابط إعادة تعيين كلمة المرور';
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في إرسال رابط إعادة التعيين'
      );
    }
  }
);

export const resetPassword = createAsyncThunk(
  'auth/resetPassword',
  async ({ token, password }, { rejectWithValue }) => {
    try {
      await authAPI.resetPassword(token, password);
      return 'تم إعادة تعيين كلمة المرور بنجاح';
    } catch (error) {
      return rejectWithValue(
        error.response?.data?.message || 'فشل في إعادة تعيين كلمة المرور'
      );
    }
  }
);

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearAuthState: (state) => {
      return { ...initialState };
    },
    setMFARequired: (state, action) => {
      state.mfaRequired = true;
      state.mfaToken = action.payload.token;
    },
    incrementLoginAttempts: (state) => {
      state.loginAttempts += 1;
    },
    resetLoginAttempts: (state) => {
      state.loginAttempts = 0;
    },
    updateUserPermissions: (state, action) => {
      state.permissions = action.payload;
    },
    setSessionExpiry: (state, action) => {
      state.sessionExpiry = action.payload;
    },
    checkTokenExpiry: (state) => {
      if (state.sessionExpiry && new Date() > new Date(state.sessionExpiry)) {
        return { ...initialState };
      }
    }
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
        state.refreshToken = action.payload.refreshToken;
        state.permissions = action.payload.permissions;
        state.sessionExpiry = action.payload.sessionExpiry;
        state.lastLoginTime = new Date().toISOString();
        state.loginAttempts = 0;
        state.mfaRequired = false;
        state.mfaToken = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
        state.loginAttempts += 1;
        
        // Check for MFA requirement
        if (action.payload?.includes('MFA') || action.payload?.includes('التحقق')) {
          state.mfaRequired = true;
          state.mfaToken = action.meta?.mfaToken;
        }
      })
      
      // Register
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
        state.refreshToken = action.payload.refreshToken;
        state.permissions = action.payload.permissions;
        state.lastLoginTime = new Date().toISOString();
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Refresh Token
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.token = action.payload.token;
        state.sessionExpiry = action.payload.sessionExpiry;
      })
      .addCase(refreshToken.rejected, (state) => {
        // Token refresh failed, logout user
        return { ...initialState };
      })
      
      // Logout
      .addCase(logoutUser.fulfilled, (state) => {
        return { ...initialState };
      })
      
      // Update Profile
      .addCase(updateProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = { ...state.user, ...action.payload };
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Change Password
      .addCase(changePassword.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(changePassword.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(changePassword.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Verify MFA
      .addCase(verifyMFA.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(verifyMFA.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
        state.refreshToken = action.payload.refreshToken;
        state.permissions = action.payload.permissions;
        state.mfaRequired = false;
        state.mfaToken = null;
        state.lastLoginTime = new Date().toISOString();
      })
      .addCase(verifyMFA.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Password Reset Request
      .addCase(requestPasswordReset.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(requestPasswordReset.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(requestPasswordReset.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      
      // Password Reset
      .addCase(resetPassword.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(resetPassword.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(resetPassword.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  }
});

// Export actions
export const {
  clearError,
  clearAuthState,
  setMFARequired,
  incrementLoginAttempts,
  resetLoginAttempts,
  updateUserPermissions,
  setSessionExpiry,
  checkTokenExpiry
} = authSlice.actions;

// Selectors
export const selectAuth = (state) => state.auth;
export const selectUser = (state) => state.auth.user;
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated;
export const selectAuthLoading = (state) => state.auth.isLoading;
export const selectAuthError = (state) => state.auth.error;
export const selectUserPermissions = (state) => state.auth.permissions;
export const selectMFARequired = (state) => state.auth.mfaRequired;
export const selectLoginAttempts = (state) => state.auth.loginAttempts;

// Complex selectors
export const selectHasPermission = (permission) => (state) => {
  return state.auth.permissions.includes(permission);
};

export const selectIsSessionValid = (state) => {
  const { sessionExpiry, isAuthenticated } = state.auth;
  if (!isAuthenticated || !sessionExpiry) return false;
  return new Date() < new Date(sessionExpiry);
};

export const selectUserRole = (state) => {
  return state.auth.user?.role || 'user';
};

export const selectIsAdmin = (state) => {
  const role = selectUserRole(state);
  return role === 'admin' || role === 'super_admin';
};

export const selectCanManageProducts = (state) => {
  return selectHasPermission('manage_products')(state) || selectIsAdmin(state);
};

export const selectCanManageOrders = (state) => {
  return selectHasPermission('manage_orders')(state) || selectIsAdmin(state);
};

export const selectCanViewReports = (state) => {
  return selectHasPermission('view_reports')(state) || selectIsAdmin(state);
};

export default authSlice.reducer;
