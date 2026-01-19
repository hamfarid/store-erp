/**
 * Layout Components Index
 * 
 * Exports all layout components for easy importing
 * 
 * Version: 3.0.0
 * Updated: 2025-12-05
 */

export { default as Navbar } from './Navbar';
export { default as Sidebar } from './Sidebar';
export { default as Footer } from './Footer';

// Default export for convenience
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Footer from './Footer';

const Layout = {
  Navbar,
  Sidebar,
  Footer
};

export default Layout;

