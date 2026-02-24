# ⚛️ React Component Structure (Global System v26 Diamond 32)

**Status:** MANDATORY
**Enforcement:** Automated by Sentinel (Linter)

## 1. The Philosophy
A component is a self-contained universe. It owns its styles, tests, and logic.

## 2. Folder Structure (The Pod)
Every component MUST live in its own directory:
```
components/
├── Button/
│   ├── Button.tsx        # Logic & View
│   ├── Button.test.tsx   # Verification
│   ├── Button.module.css # Styles (if not using Tailwind)
│   └── index.ts          # Public API
```

## 3. Component Example
```typescript
// Button.tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  // Sentinel Check: Accessibility attributes are mandatory
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
    >
      {label}
    </button>
  );
};
```

## 4. Test Example (Mandatory)
```typescript
// Button.test.tsx
import { render, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  const { getByText } = render(<Button label="Click me" onClick={handleClick} />);
  
  fireEvent.click(getByText('Click me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```
