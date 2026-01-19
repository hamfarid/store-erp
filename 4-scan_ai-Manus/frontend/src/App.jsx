/**
 * Main Application Component
 * ===========================
 * 
 * Root component that sets up routing, auth, and global providers.
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import MainLayout from './components/Layout/MainLayout';
import AppRoutes, { routeConfig } from './routes';

// Initialize theme and language
const initializeApp = () => {
  // Theme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }

  // Language/RTL
  const savedLang = localStorage.getItem('lang') || 'en';
  document.documentElement.dir = savedLang === 'ar' ? 'rtl' : 'ltr';
  document.documentElement.lang = savedLang;
};

// Initialize on load
initializeApp();

/**
 * App Component
 */
const App = () => {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Allow a brief moment for styles to load
    setTimeout(() => setReady(true), 100);
  }, []);

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center animate-pulse">
          <svg className="w-8 h-8 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
