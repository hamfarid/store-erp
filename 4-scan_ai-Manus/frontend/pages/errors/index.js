// Error Pages Index
// Exports all error page components for easy importing

export { default as Error401 } from './Error401';
export { default as Error402 } from './Error402';
export { default as Error403 } from './Error403';
export { default as Error404 } from './Error404';
export { default as Error405 } from './Error405';
export { default as Error406 } from './Error406';
export { default as Error500 } from './Error500';
export { default as Error501 } from './Error501';
export { default as Error502 } from './Error502';
export { default as Error503 } from './Error503';
export { default as Error504 } from './Error504';
export { default as Error505 } from './Error505';
export { default as Error506 } from './Error506';

// Error code to component mapping
export const ErrorPages = {
  401: Error401,
  402: Error402,
  403: Error403,
  404: Error404,
  405: Error405,
  406: Error406,
  500: Error500,
  501: Error501,
  502: Error502,
  503: Error503,
  504: Error504,
  505: Error505,
  506: Error506,
};

// Get error component by code
export const getErrorComponent = (code) => {
  return ErrorPages[code] || Error500;
};

