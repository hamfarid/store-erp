#!/usr/bin/env node

/**
 * Script to fix TypeScript compilation errors in the admin panel
 * This script addresses common issues with Babel and TypeScript compatibility
 */

const fs = require('fs');
const path = require('path');

console.log('🔧 Starting TypeScript fixes...');

// Function to create directory if it doesn't exist
function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`✅ Created directory: ${dirPath}`);
  }
}

// Function to create or update file
function createOrUpdateFile(filePath, content) {
  try {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✅ Created/Updated: ${filePath}`);
  } catch (error) {
    console.error(`❌ Error creating ${filePath}:`, error.message);
  }
}

// Ensure types directory exists
const typesDir = path.join(__dirname, 'src', 'types');
ensureDirectoryExists(typesDir);

// Create missing type definition files for Babel modules
const babelTypesContent = `
// Auto-generated type definitions for missing Babel modules

declare module '@babel/core/src/config/files/types' {
  export interface ConfigFile {
    filepath: string;
    dirname: string;
    options: any;
  }
  export interface IgnoreFile {
    filepath: string;
    dirname: string;
    ignore: any;
  }
  export interface RelativeConfig {
    config: ConfigFile | null;
    ignore: IgnoreFile | null;
  }
  export interface FilePackageData {
    filepath: string;
    directories: string[];
    pkg: any;
    isPackage: boolean;
  }
}

declare module '@babel/core/src/config/validation/options' {
  export interface CallerMetadata {
    name: string;
    [key: string]: any;
  }
}

declare module '@babel/core/src/config/files/plugins' {
  export interface PluginData {
    filepath: string;
    value: any;
  }
}

declare module '@babel/core/src/config/files/configuration' {
  export interface ConfigurationData {
    config: any;
    ignore: any;
  }
}

declare module '@babel/core/src/config/files/package' {
  export interface PackageData {
    filepath: string;
    pkg: any;
  }
}
`;

createOrUpdateFile(path.join(typesDir, 'babel-modules.d.ts'), babelTypesContent);

// Create gensync type definitions
const gensyncTypesContent = `
// Type definitions for gensync module

declare module 'gensync' {
  export interface Handler<T> extends Generator<any, T, any> {
    (): T;
  }
  
  export function sync<T>(fn: () => Handler<T>): () => T;
  export function async<T>(fn: () => Handler<T>): () => Promise<T>;
  
  export default function gensync<T>(fn: () => Handler<T>): {
    sync: () => T;
    async: () => Promise<T>;
    errback: (callback: (err: Error | null, result?: T) => void) => void;
  };
}
`;

createOrUpdateFile(path.join(typesDir, 'gensync.d.ts'), gensyncTypesContent);

// Create Babel helper compilation targets types
const compilationTargetsContent = `
// Type definitions for @babel/helper-compilation-targets

declare module '@babel/helper-compilation-targets' {
  export interface InputTargets {
    browsers?: string | string[];
    node?: string | boolean;
    chrome?: string;
    firefox?: string;
    safari?: string;
    edge?: string;
    ie?: string;
    ios?: string;
    android?: string;
    electron?: string;
    [key: string]: string | boolean | string[] | undefined;
  }

  export interface Targets {
    [key: string]: string;
  }

  export default function getTargets(
    inputTargets?: InputTargets,
    options?: {
      configPath?: string;
      ignoreBrowserslistConfig?: boolean;
      browserslistEnv?: string;
    }
  ): Targets;

  export { InputTargets, Targets };
}
`;

createOrUpdateFile(path.join(typesDir, 'compilation-targets.d.ts'), compilationTargetsContent);

console.log('🎉 TypeScript fixes completed!');
console.log('');
console.log('Next steps:');
console.log('1. Run: npm install');
console.log('2. Run: npm run type-check');
console.log('3. Run: npm start');
console.log('');
console.log('If you still see TypeScript errors, they should now be limited to your source code only.');
