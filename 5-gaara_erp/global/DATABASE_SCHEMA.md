# مخطط قاعدة البيانات - Gaara ERP v12

## نظرة عامة
مخطط شامل لقاعدة البيانات مع جميع الجداول والعلاقات في نظام Gaara ERP v12.

## 1. الجداول الأساسية

### 1.1 جدول المستخدمين (users_user)
- id (Primary Key)
- username (Unique)
- email (Unique)
- first_name
- last_name
- is_active
- date_joined
- last_login

### 1.2 جدول الشركات (core_company)
- id (Primary Key)
- name
- code
- address
- phone
- email
- tax_number

## 2. جداول المحاسبة

### 2.1 جدول الحسابات (accounting_account)
- id (Primary Key)
- code (Unique)
- name
- account_type
- parent_id (Foreign Key to self)
- company_id (Foreign Key to Company)

### 2.2 جدول القيود اليومية (accounting_journalentry)
- id (Primary Key)
- name
- date
- reference
- state
- company_id (Foreign Key to Company)

## 3. جداول المخزون

### 3.1 جدول المنتجات (inventory_product)
- id (Primary Key)
- name
- code (Unique)
- category_id (Foreign Key to ProductCategory)
- unit_price
- cost_price
- is_active

### 3.2 جدول حركات المخزون (inventory_stockmove)
- id (Primary Key)
- product_id (Foreign Key to Product)
- quantity
- date
- move_type
- reference

## 4. جداول المبيعات

### 4.1 جدول العملاء (sales_customer)
- id (Primary Key)
- name
- email
- phone
- address
- tax_number
- is_active

### 4.2 جدول أوامر البيع (sales_salesorder)
- id (Primary Key)
- name (Unique)
- customer_id (Foreign Key to Customer)
- date_order
- state
- total_amount

## 5. العلاقات الرئيسية
- Company → Users (One-to-Many)
- Account → JournalEntryLines (One-to-Many)
- Product → StockMoves (One-to-Many)
- Customer → SalesOrders (One-to-Many)

---
**تاريخ التوثيق**: نوفمبر 2025
**إصدار النظام**: Gaara ERP v12 Enhanced Security Edition
