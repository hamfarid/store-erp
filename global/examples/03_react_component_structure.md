# React Component Structure

## Folder Structure

\`\`\`
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.test.tsx
│   ├── Button.module.css
│   └── index.ts
\`\`\`

## Component Example

\`\`\`typescript
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
  return (
    <button
      className={\`\${styles.button} \${styles[variant]}\`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};
\`\`\`

## Test Example

\`\`\`typescript
// Button.test.tsx
import { render, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  const { getByText } = render(<Button label="Click me" onClick={handleClick} />);
  
  fireEvent.click(getByText('Click me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
\`\`\`
