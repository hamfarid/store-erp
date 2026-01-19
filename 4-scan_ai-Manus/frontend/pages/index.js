/**
 * Pages Index
 * ===========
 * 
 * Central export for all page components.
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

// Auth Pages
export { default as Login } from './Login';
export { default as Register } from './Register';
export { default as ForgotPassword } from './ForgotPassword';
export { default as ResetPassword } from './ResetPassword';
export { default as SetupWizard } from './SetupWizard';

// Dashboard
export { default as Dashboard } from './Dashboard';

// Farm Management
export { default as Farms } from './Farms';
export { default as Crops } from './Crops';
export { default as Equipment } from './Equipment';
export { default as Inventory } from './Inventory';
export { default as Sensors } from './Sensors';

// Diagnosis & Diseases
export { default as Diagnosis } from './Diagnosis';
export { default as Diseases } from './Diseases';

// Analytics & Reports
export { default as Analytics } from './Analytics';
export { default as Reports } from './Reports';

// Administration
export { default as Users } from './Users';
export { default as Companies } from './Companies';
export { default as Breeding } from './Breeding';

// User Pages
export { default as Profile } from './Profile';
export { default as Settings } from './Settings';

// AI/ML Pages
export { default as LearningDashboard } from './LearningDashboard';
export { default as ImageCrawler } from './ImageCrawler';

// Error Pages
export { 
  Error401, 
  Error402, 
  Error403, 
  Error404, 
  Error405, 
  Error500, 
  Error501, 
  Error502, 
  Error503, 
  Error504, 
  Error505, 
  Error506 
} from './errors';
