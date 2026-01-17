 
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true,
    'vitest-globals/env': true
  },
  extends: [
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  plugins: ['react', 'react-hooks', 'react-refresh'],
  globals: {
    process: 'readonly',
    __dirname: 'readonly',
    global: 'writable',
    globalThis: 'readonly',
    describe: 'readonly',
    test: 'readonly',
    it: 'readonly',
    expect: 'readonly',
    beforeEach: 'readonly',
    afterEach: 'readonly',
    beforeAll: 'readonly',
    afterAll: 'readonly',
    vi: 'readonly',
    jest: 'readonly',
    clients: 'readonly'
  },
  rules: {
    'no-undef': 'error',
    'no-unused-vars': ['warn', { 
      vars: 'all',
      args: 'none',  // Don't check function arguments
      ignoreRestSiblings: true,
      argsIgnorePattern: '^_',
      varsIgnorePattern: '^_'
    }],
    'react-hooks/exhaustive-deps': 'warn',
    'no-console': 'warn',
    'prefer-const': 'warn',
    'no-empty': ['warn', { allowEmptyCatch: true }],
    'react-refresh/only-export-components': 'warn'
  },
  settings: {
    react: {
      version: 'detect'
    }
  },
  overrides: [
    {
      files: ['**/__tests__/**/*', '**/*.test.{js,jsx,ts,tsx}', '**/*.spec.{js,jsx,ts,tsx}'],
      env: {
        jest: true,
        'vitest-globals/env': true
      }
    }
  ]
};
