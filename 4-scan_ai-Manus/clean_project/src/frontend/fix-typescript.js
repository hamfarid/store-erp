/**
 * fix-typescript.js
 * 
 * This script fixes TypeScript version compatibility issues.
 * Created by Fix-FrontendNpmIssue.ps1 on 2025-06-02
 */

console.log('Fixing TypeScript compatibility issues...');

// Check if we need to downgrade TypeScript
try {
  const fs = require('fs');
  const path = require('path');
  
  // Path to package.json
  const packageJsonPath = path.join(__dirname, 'package.json');
  
  if (fs.existsSync(packageJsonPath)) {
    console.log('Reading package.json...');
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    
    // Check TypeScript version
    if (packageJson.dependencies && packageJson.dependencies.typescript) {
      console.log('Current TypeScript version:', packageJson.dependencies.typescript);
      
      // Fix version if needed
      if (packageJson.dependencies.typescript.startsWith('^5')) {
        packageJson.dependencies.typescript = '^4.9.5';
        console.log('Downgraded TypeScript to ^4.9.5');
        
        // Write back to package.json
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('Updated package.json successfully');
      } else {
        console.log('TypeScript version is already compatible');
      }
    } else {
      console.log('TypeScript not found in dependencies');
    }
  } else {
    console.log('package.json not found');
  }
} catch (error) {
  console.error('Error fixing TypeScript:', error);
}

console.log('TypeScript compatibility check completed');
