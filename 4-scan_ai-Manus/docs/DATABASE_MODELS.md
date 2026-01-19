# Database Models - Gaara Scan AI v4.3

## 📋 Overview

This document describes all database models in the Gaara Scan AI system.

---

## ✅ Complete Models

### **1. User Model** (`models/user.py`)
**Purpose:** User authentication and authorization

**Fields:**
- `id` - Primary key
- `email` - Unique email address
- `password_hash` - Hashed password
- `name` - User full name
- `phone` - Phone number
- `avatar_url` - Profile picture URL
- `role` - User role (ADMIN, MANAGER, USER, GUEST)
- `mfa_secret` - MFA secret key
- `mfa_enabled` - MFA status
- `is_active` - Account status
- `is_verified` - Email verification
- `last_login_at` - Last login timestamp
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **2. Farm Model** (`models/farm.py`)
**Purpose:** Agricultural farm management

**Fields:**
- `id` - Primary key
- `owner_id` - Foreign key to User
- `name` - Farm name
- `location` - Farm location
- `address` - Full address
- `latitude`, `longitude` - GPS coordinates
- `area` - Farm area
- `area_unit` - Unit (hectare, acre)
- `crop_type` - Type of crop
- `soil_type` - Soil type
- `is_active` - Farm status
- `description`, `notes` - Additional info
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **3. Diagnosis Model** (`models/diagnosis.py`)
**Purpose:** Plant disease diagnosis records

**Fields:**
- `id` - Primary key
- `user_id` - Foreign key to User
- `farm_id` - Foreign key to Farm
- `image_url` - Diagnosis image
- `disease` - Detected disease
- `confidence` - AI confidence score
- `severity` - Disease severity
- `status` - Diagnosis status
- `model_name`, `model_version` - AI model info
- `created_at`, `updated_at` - Timestamps

---

### **4. Report Model** (`models/report.py`)
**Purpose:** Generated reports

**Fields:**
- `id` - Primary key
- `user_id` - Foreign key to User
- `title` - Report title
- `report_type` - Type of report
- `format` - File format (PDF, Excel, etc.)
- `file_url` - Report file location
- `parameters` - Report parameters (JSON)
- `created_at` - Timestamp

---

### **5. Crop Model** (`models/crop.py`) ✨ NEW
**Purpose:** Crop database and information

**Fields:**
- `id` - Primary key
- `name` - Crop name (Arabic)
- `name_en` - Crop name (English)
- `scientific_name` - Scientific name
- `category` - Category (vegetables, fruits, grains, etc.)
- `growing_season` - Growing season
- `water_needs` - Water requirements (low, medium, high)
- `sunlight_needs` - Sunlight needs (full, partial, shade)
- `temperature_min`, `temperature_max` - Temperature range
- `growth_duration` - Growth duration in days
- `description` - Crop description
- `care_tips` - Care instructions
- `common_diseases` - Common diseases (JSON)
- `image_url` - Crop image
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **6. Disease Model** (`models/disease.py`) ✨ NEW
**Purpose:** Plant disease database

**Fields:**
- `id` - Primary key
- `name` - Disease name (Arabic)
- `name_en` - Disease name (English)
- `scientific_name` - Scientific name
- `category` - Category (fungal, bacterial, viral, etc.)
- `severity` - Severity level (low, medium, high, critical)
- `symptoms` - Disease symptoms
- `causes` - Disease causes
- `treatment` - Treatment methods
- `prevention` - Prevention tips
- `affected_crops` - Affected crops (JSON)
- `image_url` - Disease image
- `cases_count` - Number of cases
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **7. Sensor Model** (`models/sensor.py`) ✨ NEW
**Purpose:** IoT sensors and readings

**Fields:**
- `id` - Primary key
- `farm_id` - Foreign key to Farm
- `name` - Sensor name
- `type` - Sensor type (temperature, humidity, etc.)
- `serial_number` - Unique serial number
- `location` - Sensor location
- `min_threshold`, `max_threshold` - Alert thresholds
- `unit` - Measurement unit
- `status` - Sensor status (active, inactive, maintenance)
- `battery_level` - Battery level (0-100)
- `value` - Current reading value
- `last_update` - Last reading timestamp
- `notes` - Additional notes
- `created_at`, `updated_at`, `deleted_at` - Timestamps

**Related Model:**
- **SensorReading** - Historical sensor readings
  - `sensor_id` - Foreign key to Sensor
  - `value` - Reading value
  - `unit` - Measurement unit
  - `timestamp` - Reading timestamp
  - `quality` - Data quality (good, warning, error)

---

### **8. Equipment Model** (`models/equipment.py`) ✨ NEW
**Purpose:** Farm equipment and machinery

**Fields:**
- `id` - Primary key
- `farm_id` - Foreign key to Farm
- `name` - Equipment name
- `type` - Equipment type (tractor, harvester, etc.)
- `brand` - Brand name
- `model` - Model number
- `serial_number` - Unique serial number
- `purchase_date` - Purchase date
- `purchase_price` - Purchase price
- `status` - Equipment status (operational, maintenance, out_of_service)
- `notes` - Additional notes
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **9. Inventory Model** (`models/inventory.py`) ✨ NEW
**Purpose:** Inventory and stock management

**Fields:**
- `id` - Primary key
- `name` - Item name
- `category` - Category (seeds, fertilizers, pesticides, etc.)
- `sku` - Stock keeping unit
- `quantity` - Current quantity
- `unit` - Unit of measurement (kg, l, pcs, etc.)
- `min_quantity` - Minimum stock threshold
- `price` - Item price
- `supplier` - Supplier name
- `location` - Storage location
- `expiry_date` - Expiry date
- `notes` - Additional notes
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **10. Company Model** (`models/company.py`) ✨ NEW
**Purpose:** Companies and business entities

**Fields:**
- `id` - Primary key
- `name` - Company name (Arabic)
- `name_en` - Company name (English)
- `type` - Company type (farm, supplier, distributor, etc.)
- `industry` - Industry sector
- `registration_number` - Business registration number
- `email` - Contact email
- `phone` - Contact phone
- `website` - Company website
- `address` - Company address
- `city` - City
- `country` - Country
- `description` - Company description
- `employees_count` - Number of employees
- `founded_year` - Year founded
- `logo_url` - Company logo
- `status` - Company status (active, inactive, pending)
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

### **11. BreedingProgram Model** (`models/breeding.py`) ✨ NEW
**Purpose:** Breeding programs and genetic improvement

**Fields:**
- `id` - Primary key
- `user_id` - Foreign key to User
- `farm_id` - Foreign key to Farm
- `name` - Program name
- `description` - Program description
- `crop_type` - Crop type
- `objective` - Program objective
- `method` - Breeding method (hybridization, selection, etc.)
- `status` - Program status (planning, in_progress, testing, completed)
- `start_date` - Start date
- `expected_end_date` - Expected end date
- `parent_varieties` - Parent varieties (JSON)
- `target_traits` - Target traits (JSON)
- `progress` - Progress percentage (0-100)
- `notes` - Additional notes
- `created_at`, `updated_at`, `deleted_at` - Timestamps

---

## 🔗 Relationships

### **User Relationships:**
- One-to-Many: Farms, Diagnoses, Reports, BreedingPrograms

### **Farm Relationships:**
- Many-to-One: User (owner)
- One-to-Many: Sensors, Equipment, BreedingPrograms, Diagnoses

### **Sensor Relationships:**
- Many-to-One: Farm
- One-to-Many: SensorReadings

---

## 📊 Database Schema Summary

| Model | Table Name | Primary Key | Foreign Keys |
|-------|-----------|-------------|--------------|
| User | `users` | `id` | - |
| Farm | `farms` | `id` | `owner_id` → users |
| Diagnosis | `diagnoses` | `id` | `user_id`, `farm_id` |
| Report | `reports` | `id` | `user_id` |
| Crop | `crops` | `id` | - |
| Disease | `diseases` | `id` | - |
| Sensor | `sensors` | `id` | `farm_id` |
| SensorReading | `sensor_readings` | `id` | `sensor_id` |
| Equipment | `equipment` | `id` | `farm_id` |
| Inventory | `inventory` | `id` | - |
| Company | `companies` | `id` | - |
| BreedingProgram | `breeding_programs` | `id` | `user_id`, `farm_id` |

---

## 🚀 Next Steps

1. **Create Alembic Migration**
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add new models: crops, diseases, sensors, equipment, inventory, companies, breeding"
   alembic upgrade head
   ```

2. **Update API Endpoints**
   - Connect API endpoints to actual database queries
   - Implement CRUD operations using SQLAlchemy models

3. **Add Relationships**
   - Define SQLAlchemy relationships in models
   - Update foreign key constraints

4. **Add Indexes**
   - Add database indexes for frequently queried fields
   - Optimize query performance

---

## ✅ Status

**Database Models:** ✅ **COMPLETE**

- ✅ 11 models created
- ✅ All fields defined
- ✅ Relationships prepared
- ✅ Timestamps included
- ✅ Soft delete support
- ✅ Ready for migrations

---

**Last Updated:** December 2024  
**Version:** 4.3.0

