/**
 * PrintButton Component
 * @file frontend/src/components/common/PrintButton.jsx
 * 
 * زر الطباعة مع دعم خيارات متعددة
 */

import React, { useState, useCallback } from 'react';
import { Printer, FileDown, ChevronDown } from 'lucide-react';
import { Button } from '../ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '../ui/dropdown-menu';

/**
 * PrintButton - زر الطباعة مع قائمة منسدلة
 */
export function PrintButton({
  onPrint,
  onExportPDF,
  onExportExcel,
  onExportCSV,
  disabled = false,
  loading = false,
  className = '',
  showDropdown = true,
  label = 'طباعة'
}) {
  const [isExporting, setIsExporting] = useState(false);

  const handleAction = useCallback(async (action, actionFn) => {
    if (!actionFn) return;
    
    setIsExporting(true);
    try {
      await actionFn();
    } catch (error) {
      console.error(`${action} failed:`, error);
    } finally {
      setIsExporting(false);
    }
  }, []);

  if (!showDropdown) {
    return (
      <Button
        variant="outline"
        onClick={() => handleAction('print', onPrint)}
        disabled={disabled || loading || isExporting}
        className={className}
      >
        <Printer className="w-4 h-4 ml-2" />
        {label}
      </Button>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          disabled={disabled || loading || isExporting}
          className={className}
        >
          <Printer className="w-4 h-4 ml-2" />
          {label}
          <ChevronDown className="w-4 h-4 mr-2" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {onPrint && (
          <DropdownMenuItem onClick={() => handleAction('print', onPrint)}>
            <Printer className="w-4 h-4 ml-2" />
            طباعة مباشرة
          </DropdownMenuItem>
        )}
        {onExportPDF && (
          <DropdownMenuItem onClick={() => handleAction('pdf', onExportPDF)}>
            <FileDown className="w-4 h-4 ml-2" />
            تصدير PDF
          </DropdownMenuItem>
        )}
        {onExportExcel && (
          <DropdownMenuItem onClick={() => handleAction('excel', onExportExcel)}>
            <FileDown className="w-4 h-4 ml-2" />
            تصدير Excel
          </DropdownMenuItem>
        )}
        {onExportCSV && (
          <DropdownMenuItem onClick={() => handleAction('csv', onExportCSV)}>
            <FileDown className="w-4 h-4 ml-2" />
            تصدير CSV
          </DropdownMenuItem>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

/**
 * PrintArea - منطقة قابلة للطباعة
 */
export function PrintArea({ children, id = 'print-area', className = '' }) {
  return (
    <div id={id} className={`print-area ${className}`}>
      {children}
    </div>
  );
}

/**
 * Hook للطباعة
 */
export function usePrint(elementId = 'print-area') {
  const print = useCallback(() => {
    const printContent = document.getElementById(elementId);
    if (!printContent) {
      console.error(`Element with id "${elementId}" not found`);
      return;
    }

    const originalContents = document.body.innerHTML;
    const printContents = printContent.innerHTML;

    document.body.innerHTML = `
      <html dir="rtl" lang="ar">
        <head>
          <title>طباعة</title>
          <style>
            @media print {
              body {
                direction: rtl;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                padding: 20px;
              }
              table {
                width: 100%;
                border-collapse: collapse;
              }
              th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: right;
              }
              th {
                background-color: #f3f4f6;
              }
              .no-print {
                display: none !important;
              }
              @page {
                margin: 1cm;
              }
            }
          </style>
        </head>
        <body>
          ${printContents}
        </body>
      </html>
    `;

    window.print();
    document.body.innerHTML = originalContents;
    window.location.reload();
  }, [elementId]);

  return { print };
}

export default PrintButton;
