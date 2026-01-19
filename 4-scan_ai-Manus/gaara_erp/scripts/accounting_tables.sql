-- إنشاء جداول وحدة الحسابات لنظام Gaara ERP

-- مخطط الحسابات
CREATE TABLE erp.chart_of_accounts (
    account_id SERIAL PRIMARY KEY,
    account_code VARCHAR(20) UNIQUE NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    parent_account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    balance_type VARCHAR(10) NOT NULL CHECK (balance_type IN ('debit', 'credit')),
    level INTEGER NOT NULL,
    is_group BOOLEAN DEFAULT FALSE,
    is_control_account BOOLEAN DEFAULT FALSE,
    is_cash_account BOOLEAN DEFAULT FALSE,
    is_bank_account BOOLEAN DEFAULT FALSE,
    is_tax_account BOOLEAN DEFAULT FALSE,
    is_system BOOLEAN DEFAULT FALSE
);

-- السنوات المالية
CREATE TABLE erp.fiscal_years (
    fiscal_year_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES erp.companies(company_id),
    year_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_closed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, year_name)
);

-- الفترات المحاسبية
CREATE TABLE erp.accounting_periods (
    period_id SERIAL PRIMARY KEY,
    fiscal_year_id INTEGER REFERENCES erp.fiscal_years(fiscal_year_id),
    period_name VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (fiscal_year_id, period_name)
);

-- دفتر اليومية
CREATE TABLE erp.journal_entries (
    entry_id SERIAL PRIMARY KEY,
    entry_number VARCHAR(20) NOT NULL,
    entry_date DATE NOT NULL,
    posting_date DATE NOT NULL,
    reference_number VARCHAR(50),
    source_document VARCHAR(50),
    source_id VARCHAR(50),
    description TEXT,
    is_posted BOOLEAN DEFAULT FALSE,
    is_reversed BOOLEAN DEFAULT FALSE,
    reversed_entry_id INTEGER REFERENCES erp.journal_entries(entry_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    period_id INTEGER REFERENCES erp.accounting_periods(period_id),
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    exchange_rate DECIMAL(18,6) DEFAULT 1,
    total_debit DECIMAL(18,2) DEFAULT 0,
    total_credit DECIMAL(18,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    approved_by INTEGER REFERENCES erp.users(user_id),
    approved_at TIMESTAMP,
    entry_type VARCHAR(50) NOT NULL,
    UNIQUE (company_id, entry_number)
);

-- بنود دفتر اليومية
CREATE TABLE erp.journal_items (
    item_id SERIAL PRIMARY KEY,
    entry_id INTEGER REFERENCES erp.journal_entries(entry_id),
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    description TEXT,
    debit DECIMAL(18,2) DEFAULT 0,
    credit DECIMAL(18,2) DEFAULT 0,
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    exchange_rate DECIMAL(18,6) DEFAULT 1,
    debit_foreign DECIMAL(18,2) DEFAULT 0,
    credit_foreign DECIMAL(18,2) DEFAULT 0,
    cost_center_id INTEGER,
    project_id INTEGER,
    dimension1_id INTEGER,
    dimension2_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- أرصدة الحسابات
CREATE TABLE erp.account_balances (
    balance_id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    period_id INTEGER REFERENCES erp.accounting_periods(period_id),
    opening_debit DECIMAL(18,2) DEFAULT 0,
    opening_credit DECIMAL(18,2) DEFAULT 0,
    period_debit DECIMAL(18,2) DEFAULT 0,
    period_credit DECIMAL(18,2) DEFAULT 0,
    closing_debit DECIMAL(18,2) DEFAULT 0,
    closing_credit DECIMAL(18,2) DEFAULT 0,
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    company_id INTEGER REFERENCES erp.companies(company_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, period_id, company_id, branch_id, currency_code)
);

-- العملاء
CREATE TABLE erp.customers (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(20),
    tax_id VARCHAR(50),
    credit_limit DECIMAL(18,2) DEFAULT 0,
    payment_terms INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, customer_code)
);

-- الموردين
CREATE TABLE erp.suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_code VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(20),
    tax_id VARCHAR(50),
    payment_terms INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, supplier_code)
);

-- فواتير المبيعات
CREATE TABLE erp.sales_invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(20) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    customer_id INTEGER REFERENCES erp.customers(customer_id),
    reference VARCHAR(50),
    description TEXT,
    subtotal DECIMAL(18,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    total_amount DECIMAL(18,2) DEFAULT 0,
    paid_amount DECIMAL(18,2) DEFAULT 0,
    balance_amount DECIMAL(18,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',
    is_posted BOOLEAN DEFAULT FALSE,
    journal_entry_id INTEGER REFERENCES erp.journal_entries(entry_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    exchange_rate DECIMAL(18,6) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, invoice_number)
);

-- بنود فواتير المبيعات
CREATE TABLE erp.sales_invoice_items (
    item_id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES erp.sales_invoices(invoice_id),
    product_id INTEGER,
    description TEXT NOT NULL,
    quantity DECIMAL(18,2) NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    tax_percent DECIMAL(5,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    total_amount DECIMAL(18,2) NOT NULL,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- فواتير المشتريات
CREATE TABLE erp.purchase_invoices (
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(20) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    supplier_id INTEGER REFERENCES erp.suppliers(supplier_id),
    reference VARCHAR(50),
    description TEXT,
    subtotal DECIMAL(18,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    total_amount DECIMAL(18,2) DEFAULT 0,
    paid_amount DECIMAL(18,2) DEFAULT 0,
    balance_amount DECIMAL(18,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft',
    is_posted BOOLEAN DEFAULT FALSE,
    journal_entry_id INTEGER REFERENCES erp.journal_entries(entry_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    exchange_rate DECIMAL(18,6) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, invoice_number)
);

-- بنود فواتير المشتريات
CREATE TABLE erp.purchase_invoice_items (
    item_id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES erp.purchase_invoices(invoice_id),
    product_id INTEGER,
    description TEXT NOT NULL,
    quantity DECIMAL(18,2) NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    discount_percent DECIMAL(5,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    tax_percent DECIMAL(5,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    total_amount DECIMAL(18,2) NOT NULL,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- المدفوعات
CREATE TABLE erp.payments (
    payment_id SERIAL PRIMARY KEY,
    payment_number VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,
    payment_type VARCHAR(20) NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    reference VARCHAR(50),
    description TEXT,
    party_type VARCHAR(20) NOT NULL,
    party_id INTEGER NOT NULL,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    is_posted BOOLEAN DEFAULT FALSE,
    journal_entry_id INTEGER REFERENCES erp.journal_entries(entry_id),
    company_id INTEGER REFERENCES erp.companies(company_id),
    branch_id INTEGER REFERENCES erp.branches(branch_id),
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    exchange_rate DECIMAL(18,6) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, payment_number)
);

-- تطبيقات المدفوعات
CREATE TABLE erp.payment_applications (
    application_id SERIAL PRIMARY KEY,
    payment_id INTEGER REFERENCES erp.payments(payment_id),
    invoice_type VARCHAR(20) NOT NULL,
    invoice_id INTEGER NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- الحسابات البنكية
CREATE TABLE erp.bank_accounts (
    bank_account_id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    bank_name VARCHAR(100) NOT NULL,
    account_number VARCHAR(50) NOT NULL,
    branch_name VARCHAR(100),
    iban VARCHAR(50),
    swift_code VARCHAR(20),
    currency_code CHAR(3) REFERENCES erp.currencies(currency_code),
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, account_number)
);

-- الضرائب
CREATE TABLE erp.taxes (
    tax_id SERIAL PRIMARY KEY,
    tax_code VARCHAR(20) NOT NULL,
    tax_name VARCHAR(100) NOT NULL,
    tax_rate DECIMAL(5,2) NOT NULL,
    account_id INTEGER REFERENCES erp.chart_of_accounts(account_id),
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, tax_code)
);

-- مراكز التكلفة
CREATE TABLE erp.cost_centers (
    cost_center_id SERIAL PRIMARY KEY,
    cost_center_code VARCHAR(20) NOT NULL,
    cost_center_name VARCHAR(100) NOT NULL,
    parent_cost_center_id INTEGER REFERENCES erp.cost_centers(cost_center_id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, cost_center_code)
);

-- الأبعاد المحاسبية
CREATE TABLE erp.dimensions (
    dimension_id SERIAL PRIMARY KEY,
    dimension_code VARCHAR(20) NOT NULL,
    dimension_name VARCHAR(100) NOT NULL,
    dimension_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    company_id INTEGER REFERENCES erp.companies(company_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (company_id, dimension_code)
);

-- قيم الأبعاد المحاسبية
CREATE TABLE erp.dimension_values (
    value_id SERIAL PRIMARY KEY,
    dimension_id INTEGER REFERENCES erp.dimensions(dimension_id),
    value_code VARCHAR(20) NOT NULL,
    value_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES erp.users(user_id),
    updated_by INTEGER REFERENCES erp.users(user_id),
    UNIQUE (dimension_id, value_code)
);

-- إدخال بعض البيانات الأساسية
INSERT INTO erp.chart_of_accounts (account_code, account_name, account_type, level, balance_type, is_group, is_system)
VALUES 
('1000', 'الأصول', 'asset', 1, 'debit', TRUE, TRUE),
('2000', 'الخصوم', 'liability', 1, 'credit', TRUE, TRUE),
('3000', 'حقوق الملكية', 'equity', 1, 'credit', TRUE, TRUE),
('4000', 'الإيرادات', 'income', 1, 'credit', TRUE, TRUE),
('5000', 'المصروفات', 'expense', 1, 'debit', TRUE, TRUE);

-- إدخال بعض الحسابات الفرعية
INSERT INTO erp.chart_of_accounts (account_code, account_name, account_type, parent_account_id, level, balance_type, is_group, is_cash_account)
VALUES 
('1100', 'النقد وما يعادله', 'asset', 1, 2, 'debit', TRUE, TRUE),
('1200', 'الذمم المدينة', 'asset', 1, 2, 'debit', TRUE, FALSE),
('1300', 'المخزون', 'asset', 1, 2, 'debit', TRUE, FALSE),
('2100', 'الذمم الدائنة', 'liability', 2, 2, 'credit', TRUE, FALSE),
('4100', 'إيرادات المبيعات', 'income', 4, 2, 'credit', FALSE, FALSE),
('5100', 'تكلفة المبيعات', 'expense', 5, 2, 'debit', FALSE, FALSE);

-- إدخال حسابات النقد
INSERT INTO erp.chart_of_accounts (account_code, account_name, account_type, parent_account_id, level, balance_type, is_group, is_cash_account, is_bank_account)
VALUES 
('1101', 'الصندوق', 'asset', 6, 3, 'debit', FALSE, TRUE, FALSE),
('1102', 'البنك', 'asset', 6, 3, 'debit', FALSE, TRUE, TRUE);
