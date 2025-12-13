// Custom type definitions
declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

declare module '*.scss' {
  const content: { [className: string]: string };
  export default content;
}

declare module '*.png' {
  const src: string;
  export default src;
}

declare module '*.jpg' {
  const src: string;
  export default src;
}

declare module '*.jpeg' {
  const src: string;
  export default src;
}

declare module '*.gif' {
  const src: string;
  export default src;
}

declare module '*.svg' {
  const src: string;
  export default src;
}

// Global types
interface Window {
  gtag?: (...args: any[]) => void;
}

// API Response types
interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// User types
interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  permissions: string[];
}

// Product types
interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  quantity: number;
  category_id?: number;
  warehouse_id?: number;
  created_at: string;
  updated_at: string;
}

export {};
