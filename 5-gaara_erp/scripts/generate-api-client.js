#!/usr/bin/env node
// FILE: scripts/generate-api-client.js | PURPOSE: Generate TypeScript API client from OpenAPI | OWNER: Frontend Team | RELATED: contracts/openapi.yaml, frontend/src/api | LAST-AUDITED: 2025-12-19
/**
 * Gaara ERP - TypeScript API Client Generator
 * 
 * Generates typed API client from OpenAPI specification
 * Usage: node scripts/generate-api-client.js
 * 
 * Features:
 * - Generates TypeScript types from OpenAPI schemas
 * - Creates typed API functions for all endpoints
 * - Includes proper error handling with unified error envelope
 * - Supports Arabic/English bilingual responses
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Paths
const OPENAPI_PATH = path.join(__dirname, '..', 'contracts', 'openapi.yaml');
const OUTPUT_DIR = path.join(__dirname, '..', 'frontend', 'src', 'api', 'generated');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

/**
 * Load OpenAPI specification
 */
function loadOpenAPI() {
    try {
        const content = fs.readFileSync(OPENAPI_PATH, 'utf8');
        return yaml.load(content);
    } catch (error) {
        console.error(`Error loading OpenAPI spec: ${error.message}`);
        process.exit(1);
    }
}

/**
 * Convert OpenAPI type to TypeScript type
 */
function toTsType(schema, schemas = {}) {
    if (!schema) return 'unknown';
    
    if (schema.$ref) {
        const refName = schema.$ref.split('/').pop();
        return refName;
    }
    
    switch (schema.type) {
        case 'string':
            if (schema.enum) {
                return schema.enum.map(e => `'${e}'`).join(' | ');
            }
            if (schema.format === 'date-time') return 'string'; // ISO date string
            if (schema.format === 'date') return 'string';
            if (schema.format === 'uuid') return 'string';
            if (schema.format === 'email') return 'string';
            return 'string';
        case 'integer':
        case 'number':
            return 'number';
        case 'boolean':
            return 'boolean';
        case 'array':
            const itemType = toTsType(schema.items, schemas);
            return `${itemType}[]`;
        case 'object':
            if (schema.properties) {
                const props = Object.entries(schema.properties).map(([key, prop]) => {
                    const required = schema.required?.includes(key);
                    const type = toTsType(prop, schemas);
                    return `  ${key}${required ? '' : '?'}: ${type};`;
                }).join('\n');
                return `{\n${props}\n}`;
            }
            if (schema.additionalProperties) {
                const valueType = toTsType(schema.additionalProperties, schemas);
                return `Record<string, ${valueType}>`;
            }
            return 'Record<string, unknown>';
        default:
            if (schema.oneOf) {
                return schema.oneOf.map(s => toTsType(s, schemas)).join(' | ');
            }
            if (schema.anyOf) {
                return schema.anyOf.map(s => toTsType(s, schemas)).join(' | ');
            }
            if (schema.allOf) {
                return schema.allOf.map(s => toTsType(s, schemas)).join(' & ');
            }
            return 'unknown';
    }
}

/**
 * Generate TypeScript interfaces from schemas
 */
function generateTypes(schemas) {
    const types = [];
    
    // Add common API response types
    types.push(`
// =============================================================================
// Gaara ERP - Generated API Types
// Generated from: contracts/openapi.yaml
// Generated at: ${new Date().toISOString()}
// =============================================================================

// Common API Response Types
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  traceId: string;
  pagination?: PaginationMeta;
}

export interface ApiError {
  success: false;
  code: string;
  message: string;
  details?: Record<string, unknown>;
  traceId: string;
}

export interface PaginationMeta {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

// Error Codes
export type ErrorCode = 
  | 'AUTH_REQUIRED'
  | 'AUTH_INVALID'
  | 'AUTH_EXPIRED'
  | 'PERMISSION_DENIED'
  | 'VALIDATION_ERROR'
  | 'NOT_FOUND'
  | 'METHOD_NOT_ALLOWED'
  | 'RATE_LIMITED'
  | 'INTERNAL_ERROR'
  | 'PARSE_ERROR'
  | 'UNSUPPORTED_MEDIA';

`);
    
    // Generate types from schemas
    for (const [name, schema] of Object.entries(schemas || {})) {
        const tsType = toTsType({ ...schema, type: 'object' }, schemas);
        
        // Add JSDoc if description exists
        const comment = schema.description 
            ? `/**\n * ${schema.description}\n */\n` 
            : '';
        
        if (schema.enum) {
            types.push(`${comment}export type ${name} = ${schema.enum.map(e => `'${e}'`).join(' | ')};\n`);
        } else {
            types.push(`${comment}export interface ${name} ${tsType}\n`);
        }
    }
    
    return types.join('\n');
}

/**
 * Convert path parameters to TypeScript function parameters
 */
function generatePathParams(path, parameters = []) {
    const pathParams = parameters.filter(p => p.in === 'path');
    const queryParams = parameters.filter(p => p.in === 'query');
    
    const params = [];
    
    // Path parameters
    for (const param of pathParams) {
        const type = toTsType(param.schema);
        params.push(`${param.name}: ${type}`);
    }
    
    // Query parameters as options object
    if (queryParams.length > 0) {
        const queryFields = queryParams.map(p => {
            const type = toTsType(p.schema);
            return `  ${p.name}${p.required ? '' : '?'}: ${type};`;
        }).join('\n');
        params.push(`options?: {\n${queryFields}\n}`);
    }
    
    return params;
}

/**
 * Generate API client functions
 */
function generateApiClient(paths, schemas) {
    const functions = [];
    
    functions.push(`
// =============================================================================
// Gaara ERP - Generated API Client
// Generated from: contracts/openapi.yaml
// Generated at: ${new Date().toISOString()}
// =============================================================================

import axios, { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios';
import * as Types from './types';

// API Client Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class GaaraApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = API_BASE_URL) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Request interceptor - add auth token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = \`Bearer \${token}\`;
      }
      return config;
    });

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<Types.ApiError>) => {
        if (error.response?.status === 401) {
          // Token expired - try refresh or redirect to login
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Set auth token
   */
  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  /**
   * Clear auth token
   */
  clearToken(): void {
    localStorage.removeItem('access_token');
  }

  /**
   * Make API request with unified error handling
   */
  private async request<T>(
    method: string,
    path: string,
    data?: unknown,
    config?: AxiosRequestConfig
  ): Promise<Types.ApiResponse<T>> {
    try {
      const response = await this.client.request<Types.ApiResponse<T>>({
        method,
        url: path,
        data,
        ...config,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return error.response.data as Types.ApiResponse<T>;
      }
      throw error;
    }
  }

`);

    // Generate functions for each endpoint
    for (const [path, methods] of Object.entries(paths || {})) {
        for (const [method, operation] of Object.entries(methods)) {
            if (['get', 'post', 'put', 'patch', 'delete'].includes(method)) {
                const funcName = operation.operationId || 
                    `${method}${path.replace(/[\/\{\}]/g, '_').replace(/-/g, '_')}`;
                
                const parameters = operation.parameters || [];
                const params = generatePathParams(path, parameters);
                
                // Add request body if present
                let bodyType = 'unknown';
                if (operation.requestBody?.content?.['application/json']?.schema) {
                    bodyType = toTsType(operation.requestBody.content['application/json'].schema);
                    if (method !== 'get') {
                        params.push(`body: ${bodyType}`);
                    }
                }
                
                // Determine response type
                let responseType = 'unknown';
                const successResponse = operation.responses?.['200'] || operation.responses?.['201'];
                if (successResponse?.content?.['application/json']?.schema) {
                    responseType = toTsType(successResponse.content['application/json'].schema);
                }
                
                // Build path with interpolation
                const interpolatedPath = path.replace(/\{(\w+)\}/g, '${$1}');
                
                // Generate function
                const paramStr = params.join(', ');
                const comment = operation.summary 
                    ? `  /**\n   * ${operation.summary}\n   * ${operation.description || ''}\n   */\n` 
                    : '';
                
                functions.push(`${comment}  async ${funcName}(${paramStr}): Promise<Types.ApiResponse<${responseType}>> {
    return this.request('${method.toUpperCase()}', \`${interpolatedPath}\`${method !== 'get' && operation.requestBody ? ', body' : ''});
  }
`);
            }
        }
    }
    
    functions.push(`}

// Export singleton instance
export const api = new GaaraApiClient();
export default api;
`);
    
    return functions.join('\n');
}

/**
 * Main generator function
 */
function main() {
    console.log('🚀 Generating TypeScript API client from OpenAPI spec...\n');
    
    const spec = loadOpenAPI();
    console.log(`📖 Loaded OpenAPI: ${spec.info?.title} v${spec.info?.version}`);
    
    // Generate types
    console.log('📝 Generating TypeScript types...');
    const types = generateTypes(spec.components?.schemas);
    fs.writeFileSync(path.join(OUTPUT_DIR, 'types.ts'), types);
    console.log(`   ✅ Generated types.ts`);
    
    // Generate API client
    console.log('📝 Generating API client...');
    const client = generateApiClient(spec.paths, spec.components?.schemas);
    fs.writeFileSync(path.join(OUTPUT_DIR, 'client.ts'), client);
    console.log(`   ✅ Generated client.ts`);
    
    // Generate index
    const index = `// Auto-generated API exports
export * from './types';
export * from './client';
export { api as default } from './client';
`;
    fs.writeFileSync(path.join(OUTPUT_DIR, 'index.ts'), index);
    console.log(`   ✅ Generated index.ts`);
    
    console.log('\n✨ API client generation complete!');
    console.log(`   Output directory: ${OUTPUT_DIR}`);
}

// Run generator
main();
