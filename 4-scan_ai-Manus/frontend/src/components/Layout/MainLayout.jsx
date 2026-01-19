/**
 * Main Layout Component
 * ======================
 * 
 * Main application layout with sidebar, header, and content area.
 * 
 * Features:
 * - Responsive sidebar
 * - Header with user menu
 * - Toast notifications
 * - RTL support
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Sidebar from '../Navigation/Sidebar';
import Header from '../Navigation/Header';
import { ToastProvider } from '../Toast';
import { useAuth } from '../../hooks/useAuth';

const MainLayout = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [notifications, setNotifications] = useState([]);

  // Load sidebar state from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('sidebarCollapsed');
    if (saved) {
      setSidebarCollapsed(JSON.parse(saved));
    }
  }, []);

  // Save sidebar state
  const handleSidebarCollapse = (collapsed) => {
    setSidebarCollapsed(collapsed);
    localStorage.setItem('sidebarCollapsed', JSON.stringify(collapsed));
  };

  // Handle logout
  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  // Handle search
  const handleSearch = (query) => {
    console.log('Search:', query);
    // Implement global search
  };

  const isRTL = document.documentElement.dir === 'rtl';

  return (
    <ToastProvider position={isRTL ? 'top-left' : 'top-right'}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
        {/* Sidebar */}
        <Sidebar
          user={user}
          collapsed={sidebarCollapsed}
          onCollapse={handleSidebarCollapse}
          onLogout={handleLogout}
        />

        {/* Main Content */}
        <div className={`
          flex-1 flex flex-col min-w-0
          transition-all duration-300
          ${sidebarCollapsed ? 'lg:ml-20 rtl:lg:ml-0 rtl:lg:mr-20' : 'lg:ml-64 rtl:lg:ml-0 rtl:lg:mr-64'}
        `}>
          {/* Header */}
          <Header
            user={user}
            notifications={notifications}
            onLogout={handleLogout}
            onSearch={handleSearch}
          />

          {/* Page Content */}
          <main className="flex-1 p-4 lg:p-6 overflow-auto">
            <Outlet />
          </main>

          {/* Footer */}
          <footer className="py-4 px-6 border-t border-gray-200 dark:border-gray-700 text-center text-sm text-gray-500 dark:text-gray-400">
            <p>
              © 2026 Gaara Scan AI. {isRTL ? 'جميع الحقوق محفوظة' : 'All rights reserved.'}
            </p>
          </footer>
        </div>
      </div>
    </ToastProvider>
  );
};

export default MainLayout;
