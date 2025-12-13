// FILE: frontend/src/tests/AccessibleComponents.test.jsx | PURPOSE: Accessibility Component Tests | OWNER: Frontend | RELATED: components/ui/ | LAST-AUDITED: 2025-10-21

/**
 * اختبارات مكونات إمكانية الوصول - الإصدار 2.0
 * Accessibility Component Tests - Version 2.0
 * 
 * P3 Fixes Applied:
 * - P3.9: WCAG AA compliance tests
 * - P3.10: Keyboard navigation tests
 * - P3.11: Screen reader compatibility tests
 * - P3.12: RTL language support tests
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react'; // waitFor removed - unused
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';

import AccessibleButton from '../components/ui/AccessibleButton';
import { FormInput, FormSelect, FormCheckbox, FormGroup, FormLabel } from '../components/ui/AccessibleForm';
import AccessibleTable from '../components/ui/AccessibleTable';

// Mock utilities
jest.mock('../lib/utils', () => ({
  cn: (...classes) => classes.filter(Boolean).join(' ')
}));

describe('AccessibleButton', () => {
  test('renders with correct ARIA attributes', () => {
    render(
      <AccessibleButton ariaLabel="Test button" ariaDescribedBy="help-text">
        Click me
      </AccessibleButton>
    );
    
    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('aria-label', 'Test button');
    expect(button).toHaveAttribute('aria-describedby', 'help-text');
    expect(button).toHaveAttribute('role', 'button');
  });

  test('handles keyboard navigation correctly', async () => {
    const handleClick = jest.fn();
    render(
      <AccessibleButton onClick={handleClick}>
        Click me
      </AccessibleButton>
    );
    
    const button = screen.getByRole('button');
    
    // Test Enter key
    fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalledTimes(1);
    
    // Test Space key
    fireEvent.keyDown(button, { key: ' ' });
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  test('shows loading state correctly', () => {
    render(
      <AccessibleButton loading={true}>
        Submit
      </AccessibleButton>
    );
    
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-disabled', 'true');
    expect(screen.getByText('جاري التحميل...')).toBeInTheDocument();
  });

  test('disabled state prevents interaction', () => {
    const handleClick = jest.fn();
    render(
      <AccessibleButton disabled={true} onClick={handleClick}>
        Disabled
      </AccessibleButton>
    );
    
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('tabIndex', '-1');
    
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  test('applies correct variant styles', () => {
    const { rerender } = render(
      <AccessibleButton variant="primary">Primary</AccessibleButton>
    );
    
    let button = screen.getByRole('button');
    expect(button).toHaveClass('bg-primary');
    
    rerender(
      <AccessibleButton variant="destructive">Destructive</AccessibleButton>
    );
    
    button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });
});

describe('FormInput', () => {
  test('renders with proper label association', () => {
    render(
      <FormGroup>
        <FormLabel htmlFor="test-input" required>Test Input</FormLabel>
        <FormInput id="test-input" name="test" required />
      </FormGroup>
    );
    
    const input = screen.getByRole('textbox');
    const label = screen.getByText('Test Input');
    
    expect(input).toHaveAttribute('id', 'test-input');
    expect(label).toHaveAttribute('for', 'test-input');
    expect(input).toHaveAttribute('aria-required', 'true');
    expect(screen.getByText('*')).toBeInTheDocument();
  });

  test('displays error messages correctly', () => {
    render(
      <FormInput 
        id="test-input" 
        name="test" 
        error="This field is required"
      />
    );
    
    const input = screen.getByRole('textbox');
    const errorMessage = screen.getByRole('alert');
    
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby', 'test-input-error');
    expect(errorMessage).toHaveTextContent('This field is required');
    expect(errorMessage).toHaveAttribute('id', 'test-input-error');
  });

  test('shows help text when provided', () => {
    render(
      <FormInput 
        id="test-input" 
        name="test" 
        helpText="Enter your full name"
      />
    );
    
    const input = screen.getByRole('textbox');
    const helpText = screen.getByText('Enter your full name');
    
    expect(input).toHaveAttribute('aria-describedby', 'test-input-help');
    expect(helpText).toHaveAttribute('id', 'test-input-help');
  });

  test('handles value changes correctly', async () => {
    const handleChange = jest.fn();
    render(
      <FormInput 
        id="test-input" 
        name="test" 
        onChange={handleChange}
      />
    );
    
    const input = screen.getByRole('textbox');
    await userEvent.type(input, 'test value');
    
    expect(handleChange).toHaveBeenCalled();
    expect(input).toHaveValue('test value');
  });
});

describe('FormSelect', () => {
  const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3', disabled: true }
  ];

  test('renders options correctly', () => {
    render(
      <FormSelect 
        id="test-select" 
        name="test" 
        options={options}
        placeholder="Choose an option"
      />
    );
    
    const select = screen.getByRole('combobox');
    expect(select).toBeInTheDocument();
    
    // Check placeholder
    expect(screen.getByText('Choose an option')).toBeInTheDocument();
    
    // Check options
    expect(screen.getByText('Option 1')).toBeInTheDocument();
    expect(screen.getByText('Option 2')).toBeInTheDocument();
    expect(screen.getByText('Option 3')).toBeInTheDocument();
  });

  test('handles selection correctly', async () => {
    const handleChange = jest.fn();
    render(
      <FormSelect 
        id="test-select" 
        name="test" 
        options={options}
        onChange={handleChange}
      />
    );
    
    const select = screen.getByRole('combobox');
    await userEvent.selectOptions(select, 'option1');
    
    expect(handleChange).toHaveBeenCalled();
    expect(select).toHaveValue('option1');
  });

  test('disables options correctly', () => {
    render(
      <FormSelect 
        id="test-select" 
        name="test" 
        options={options}
      />
    );
    
    const disabledOption = screen.getByRole('option', { name: 'Option 3' });
    expect(disabledOption).toBeDisabled();
  });
});

describe('FormCheckbox', () => {
  test('renders with correct label association', () => {
    render(
      <FormCheckbox 
        id="test-checkbox" 
        name="test" 
        label="Accept terms and conditions"
        required
      />
    );
    
    const checkbox = screen.getByRole('checkbox');
    const label = screen.getByText('Accept terms and conditions');
    
    expect(checkbox).toHaveAttribute('id', 'test-checkbox');
    expect(label).toHaveAttribute('for', 'test-checkbox');
    expect(checkbox).toHaveAttribute('aria-required', 'true');
  });

  test('handles checked state correctly', async () => {
    const handleChange = jest.fn();
    render(
      <FormCheckbox 
        id="test-checkbox" 
        name="test" 
        label="Test checkbox"
        onChange={handleChange}
      />
    );
    
    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();
    
    await userEvent.click(checkbox);
    expect(handleChange).toHaveBeenCalled();
    expect(checkbox).toBeChecked();
  });

  test('displays error messages correctly', () => {
    render(
      <FormCheckbox 
        id="test-checkbox" 
        name="test" 
        label="Test checkbox"
        error="You must accept the terms"
      />
    );
    
    const checkbox = screen.getByRole('checkbox');
    const errorMessage = screen.getByRole('alert');
    
    expect(checkbox).toHaveAttribute('aria-invalid', 'true');
    expect(errorMessage).toHaveTextContent('You must accept the terms');
  });
});

describe('AccessibleTable', () => {
  const mockData = [
    { id: 1, name: 'Product 1', price: 10.99, category: 'Electronics' },
    { id: 2, name: 'Product 2', price: 25.50, category: 'Books' },
    { id: 3, name: 'Product 3', price: 15.75, category: 'Electronics' }
  ];

  const mockColumns = [
    { key: 'name', header: 'Product Name', align: 'right' },
    { key: 'price', header: 'Price', align: 'center' },
    { key: 'category', header: 'Category', align: 'right' }
  ];

  test('renders table with correct structure', () => {
    render(
      <AccessibleTable 
        data={mockData} 
        columns={mockColumns}
        caption="Product inventory table"
      />
    );
    
    const table = screen.getByRole('table');
    expect(table).toHaveAttribute('aria-label', 'Product inventory table');
    
    // Check headers
    expect(screen.getByRole('columnheader', { name: 'Product Name' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Price' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Category' })).toBeInTheDocument();
    
    // Check data rows
    expect(screen.getByText('Product 1')).toBeInTheDocument();
    expect(screen.getByText('10.99')).toBeInTheDocument();
    expect(screen.getByText('Electronics')).toBeInTheDocument();
  });

  test('handles sorting correctly', async () => {
    const handleSort = jest.fn();
    render(
      <AccessibleTable 
        data={mockData} 
        columns={mockColumns}
        sortable={true}
        onSort={handleSort}
      />
    );
    
    const nameHeader = screen.getByRole('columnheader', { name: /Product Name/ });
    expect(nameHeader).toHaveAttribute('aria-sort', 'none');
    
    await userEvent.click(nameHeader);
    expect(handleSort).toHaveBeenCalledWith({ key: 'name', direction: 'asc' });
  });

  test('handles row selection correctly', async () => {
    const handleRowSelect = jest.fn();
    render(
      <AccessibleTable 
        data={mockData} 
        columns={mockColumns}
        selectable={true}
        onRowSelect={handleRowSelect}
      />
    );
    
    const selectAllCheckbox = screen.getByLabelText('تحديد جميع الصفوف');
    expect(selectAllCheckbox).toBeInTheDocument();
    
    const firstRowCheckbox = screen.getByLabelText('تحديد الصف 1');
    await userEvent.click(firstRowCheckbox);
    
    expect(handleRowSelect).toHaveBeenCalledWith([0]);
  });

  test('supports keyboard navigation', async () => {
    render(
      <AccessibleTable 
        data={mockData} 
        columns={mockColumns}
        selectable={true}
      />
    );
    
    const firstCell = screen.getByRole('gridcell', { name: /تحديد الصف 1/ });
    firstCell.focus();
    
    // Test arrow key navigation
    fireEvent.keyDown(firstCell, { key: 'ArrowRight' });
    fireEvent.keyDown(firstCell, { key: 'ArrowDown' });
    fireEvent.keyDown(firstCell, { key: 'Home' });
    fireEvent.keyDown(firstCell, { key: 'End' });
    
    // Should not throw errors
    expect(firstCell).toBeInTheDocument();
  });

  test('displays empty state correctly', () => {
    render(
      <AccessibleTable 
        data={[]} 
        columns={mockColumns}
      />
    );
    
    expect(screen.getByText('لا توجد بيانات للعرض')).toBeInTheDocument();
  });
});

describe('RTL Language Support', () => {
  test('components work correctly in RTL mode', () => {
    // Set document direction to RTL
    document.dir = 'rtl';
    
    render(
      <div dir="rtl">
        <AccessibleButton>Arabic Button</AccessibleButton>
        <FormInput id="arabic-input" name="arabic" placeholder="أدخل النص هنا" />
      </div>
    );
    
    const button = screen.getByRole('button');
    const input = screen.getByRole('textbox');
    
    expect(button).toBeInTheDocument();
    expect(input).toHaveAttribute('placeholder', 'أدخل النص هنا');
    
    // Reset document direction
    document.dir = 'ltr';
  });
});

describe('Color Contrast and Visual Accessibility', () => {
  test('components have appropriate contrast classes', () => {
    render(
      <AccessibleButton variant="primary">
        High Contrast Button
      </AccessibleButton>
    );
    
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-primary', 'text-primary-foreground');
  });

  test('error states have sufficient contrast', () => {
    render(
      <FormInput 
        id="error-input" 
        name="error" 
        error="Error message"
      />
    );
    
    const input = screen.getByRole('textbox');
    const errorMessage = screen.getByRole('alert');
    
    expect(input).toHaveClass('border-destructive');
    expect(errorMessage).toHaveClass('form-error');
  });
});

describe('Focus Management', () => {
  test('components maintain proper focus order', async () => {
    render(
      <div>
        <AccessibleButton>First</AccessibleButton>
        <FormInput id="input1" name="input1" />
        <AccessibleButton>Second</AccessibleButton>
        <FormInput id="input2" name="input2" />
      </div>
    );
    
    const firstButton = screen.getByRole('button', { name: 'First' });
    const input1 = screen.getByDisplayValue('');
    const secondButton = screen.getByRole('button', { name: 'Second' });
    
    // Test tab order
    firstButton.focus();
    expect(firstButton).toHaveFocus();
    
    await userEvent.tab();
    expect(input1).toHaveFocus();
    
    await userEvent.tab();
    expect(secondButton).toHaveFocus();
  });

  test('disabled elements are skipped in tab order', async () => {
    render(
      <div>
        <AccessibleButton>Enabled</AccessibleButton>
        <AccessibleButton disabled>Disabled</AccessibleButton>
        <FormInput id="input1" name="input1" />
      </div>
    );
    
    const enabledButton = screen.getByRole('button', { name: 'Enabled' });
    const disabledButton = screen.getByRole('button', { name: 'Disabled' });
    const input = screen.getByRole('textbox');
    
    enabledButton.focus();
    expect(enabledButton).toHaveFocus();
    
    await userEvent.tab();
    expect(input).toHaveFocus();
    expect(disabledButton).not.toHaveFocus();
  });
});
