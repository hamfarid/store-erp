/**
 * Context Exports Index
 * 
 * Central export for all context providers
 * 
 * Version: 3.0.0
 * Updated: 2025-12-05
 */

export { AuthContext, AuthProvider, useAuth } from './AuthContext';
export { DataProvider, useData } from './DataContext';

// For backward compatibility - re-export default from AuthContext
import AuthContext from './AuthContext';
export default AuthContext;

