-- إنشاء جداول وحدة المشاتل والمزارع لنظام Gaara ERP
-- تاريخ الإنشاء: 27 أبريل 2025

-- جدول المشاتل
CREATE TABLE IF NOT EXISTS nurseries (
    nursery_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    area DECIMAL(10, 2) NOT NULL COMMENT 'المساحة بالمتر المربع',
    capacity INTEGER NOT NULL COMMENT 'السعة الإجمالية للنباتات',
    manager_id INTEGER REFERENCES employees(employee_id),
    establishment_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'under_maintenance')),
    irrigation_system VARCHAR(50),
    temperature_control BOOLEAN DEFAULT FALSE,
    humidity_control BOOLEAN DEFAULT FALSE,
    light_control BOOLEAN DEFAULT FALSE,
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    branch_id INTEGER NOT NULL REFERENCES branches(branch_id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(user_id),
    updated_by INTEGER REFERENCES users(user_id)
);

-- جدول أقسام المشتل
CREATE TABLE IF NOT EXISTS nursery_sections (
    section_id SERIAL PRIMARY KEY,
    nursery_id INTEGER NOT NULL REFERENCES nurseries(nursery_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    area DECIMAL(10, 2) NOT NULL COMMENT 'المساحة بالمتر المربع',
    capacity INTEGER NOT NULL COMMENT 'السعة الإجمالية للنباتات',
    section_type VARCHAR(50) NOT NULL COMMENT 'نوع القسم: بذور، شتلات، نباتات بالغة، إلخ',
    temperature_range VARCHAR(50) COMMENT 'نطاق درجة الحرارة المثالي',
    humidity_range VARCHAR(50) COMMENT 'نطاق الرطوبة المثالي',
    light_conditions VARCHAR(50) COMMENT 'ظروف الإضاءة',
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'under_maintenance')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول أنواع النباتات
CREATE TABLE IF NOT EXISTS plant_types (
    plant_type_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    category VARCHAR(50) NOT NULL COMMENT 'فئة النبات: خضروات، فواكه، زينة، إلخ',
    growth_period INTEGER COMMENT 'فترة النمو بالأيام',
    optimal_temperature VARCHAR(50) COMMENT 'درجة الحرارة المثلى',
    optimal_humidity VARCHAR(50) COMMENT 'الرطوبة المثلى',
    optimal_light VARCHAR(50) COMMENT 'الإضاءة المثلى',
    planting_seasons VARCHAR(100) COMMENT 'مواسم الزراعة',
    description TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول مخزون المشتل
CREATE TABLE IF NOT EXISTS nursery_inventory (
    inventory_id SERIAL PRIMARY KEY,
    nursery_id INTEGER NOT NULL REFERENCES nurseries(nursery_id),
    section_id INTEGER REFERENCES nursery_sections(section_id),
    plant_type_id INTEGER NOT NULL REFERENCES plant_types(plant_type_id),
    batch_number VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    planting_date DATE NOT NULL,
    expected_maturity_date DATE,
    status VARCHAR(30) NOT NULL DEFAULT 'growing' CHECK (status IN ('seed', 'growing', 'mature', 'sold', 'damaged', 'discarded')),
    source VARCHAR(50) COMMENT 'مصدر النباتات: إنتاج ذاتي، شراء، إلخ',
    cost_per_unit DECIMAL(10, 2) NOT NULL,
    selling_price DECIMAL(10, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المزارع
CREATE TABLE IF NOT EXISTS farms (
    farm_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    area DECIMAL(10, 2) NOT NULL COMMENT 'المساحة بالهكتار',
    manager_id INTEGER REFERENCES employees(employee_id),
    establishment_date DATE NOT NULL,
    soil_type VARCHAR(50),
    water_source VARCHAR(50),
    irrigation_system VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'under_maintenance')),
    company_id INTEGER NOT NULL REFERENCES companies(company_id),
    branch_id INTEGER NOT NULL REFERENCES branches(branch_id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(user_id),
    updated_by INTEGER REFERENCES users(user_id)
);

-- جدول قطع الأراضي في المزرعة
CREATE TABLE IF NOT EXISTS farm_plots (
    plot_id SERIAL PRIMARY KEY,
    farm_id INTEGER NOT NULL REFERENCES farms(farm_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    area DECIMAL(10, 2) NOT NULL COMMENT 'المساحة بالهكتار',
    soil_type VARCHAR(50),
    irrigation_method VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'planted', 'fallow', 'under_maintenance')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المحاصيل
CREATE TABLE IF NOT EXISTS crops (
    crop_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    category VARCHAR(50) NOT NULL COMMENT 'فئة المحصول: حبوب، خضروات، فواكه، إلخ',
    growth_period INTEGER COMMENT 'فترة النمو بالأيام',
    planting_depth DECIMAL(5, 2) COMMENT 'عمق الزراعة بالسنتيمتر',
    row_spacing DECIMAL(5, 2) COMMENT 'المسافة بين الصفوف بالسنتيمتر',
    plant_spacing DECIMAL(5, 2) COMMENT 'المسافة بين النباتات بالسنتيمتر',
    water_requirements VARCHAR(50) COMMENT 'متطلبات الري',
    optimal_temperature VARCHAR(50) COMMENT 'درجة الحرارة المثلى',
    planting_seasons VARCHAR(100) COMMENT 'مواسم الزراعة',
    description TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول زراعات المزرعة
CREATE TABLE IF NOT EXISTS farm_plantings (
    planting_id SERIAL PRIMARY KEY,
    farm_id INTEGER NOT NULL REFERENCES farms(farm_id),
    plot_id INTEGER NOT NULL REFERENCES farm_plots(plot_id),
    crop_id INTEGER NOT NULL REFERENCES crops(crop_id),
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    quantity_planted DECIMAL(10, 2) NOT NULL COMMENT 'الكمية المزروعة (بذور/شتلات)',
    quantity_unit VARCHAR(20) NOT NULL COMMENT 'وحدة قياس الكمية المزروعة',
    expected_yield DECIMAL(10, 2) COMMENT 'المحصول المتوقع',
    actual_yield DECIMAL(10, 2) COMMENT 'المحصول الفعلي',
    yield_unit VARCHAR(20) COMMENT 'وحدة قياس المحصول',
    status VARCHAR(30) NOT NULL DEFAULT 'planted' CHECK (status IN ('planned', 'planted', 'growing', 'harvested', 'failed')),
    source VARCHAR(50) COMMENT 'مصدر البذور/الشتلات',
    cost_per_unit DECIMAL(10, 2) NOT NULL,
    estimated_revenue DECIMAL(10, 2),
    actual_revenue DECIMAL(10, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول الأنشطة الزراعية
CREATE TABLE IF NOT EXISTS agricultural_activities (
    activity_id SERIAL PRIMARY KEY,
    planting_id INTEGER REFERENCES farm_plantings(planting_id),
    inventory_id INTEGER REFERENCES nursery_inventory(inventory_id),
    activity_type VARCHAR(50) NOT NULL COMMENT 'نوع النشاط: ري، تسميد، مكافحة آفات، حصاد، إلخ',
    activity_date DATE NOT NULL,
    description TEXT NOT NULL,
    materials_used TEXT COMMENT 'المواد المستخدمة',
    quantity_used DECIMAL(10, 2) COMMENT 'كمية المواد المستخدمة',
    quantity_unit VARCHAR(20) COMMENT 'وحدة قياس الكمية',
    cost DECIMAL(10, 2) COMMENT 'تكلفة النشاط',
    performed_by INTEGER REFERENCES employees(employee_id),
    status VARCHAR(20) NOT NULL DEFAULT 'completed' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المعدات الزراعية
CREATE TABLE IF NOT EXISTS agricultural_equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    equipment_type VARCHAR(50) NOT NULL,
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    purchase_date DATE,
    purchase_cost DECIMAL(10, 2),
    expected_lifetime INTEGER COMMENT 'العمر المتوقع بالسنوات',
    current_status VARCHAR(30) NOT NULL DEFAULT 'operational' CHECK (status IN ('operational', 'under_maintenance', 'out_of_service', 'retired')),
    location_id INTEGER COMMENT 'موقع المعدة (مشتل أو مزرعة)',
    location_type VARCHAR(20) COMMENT 'نوع الموقع: مشتل أو مزرعة',
    maintenance_schedule TEXT,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المواد الزراعية
CREATE TABLE IF NOT EXISTS agricultural_supplies (
    supply_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    supply_type VARCHAR(50) NOT NULL COMMENT 'نوع المادة: سماد، مبيد، بذور، إلخ',
    manufacturer VARCHAR(100),
    unit VARCHAR(20) NOT NULL COMMENT 'وحدة القياس',
    quantity_in_stock DECIMAL(10, 2) NOT NULL,
    reorder_level DECIMAL(10, 2) NOT NULL,
    cost_per_unit DECIMAL(10, 2) NOT NULL,
    location_id INTEGER COMMENT 'موقع التخزين',
    location_type VARCHAR(20) COMMENT 'نوع موقع التخزين',
    expiry_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول حركات المواد الزراعية
CREATE TABLE IF NOT EXISTS supply_movements (
    movement_id SERIAL PRIMARY KEY,
    supply_id INTEGER NOT NULL REFERENCES agricultural_supplies(supply_id),
    movement_type VARCHAR(20) NOT NULL CHECK (movement_type IN ('purchase', 'consumption', 'transfer', 'adjustment')),
    quantity DECIMAL(10, 2) NOT NULL,
    movement_date DATE NOT NULL,
    source_location_id INTEGER,
    source_location_type VARCHAR(20),
    destination_location_id INTEGER,
    destination_location_type VARCHAR(20),
    reference_id INTEGER COMMENT 'مرجع للنشاط أو الطلب المرتبط',
    reference_type VARCHAR(50) COMMENT 'نوع المرجع',
    unit_cost DECIMAL(10, 2),
    total_cost DECIMAL(10, 2),
    performed_by INTEGER REFERENCES employees(employee_id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول تكامل مع نظام الذكاء الاصطناعي الزراعي
CREATE TABLE IF NOT EXISTS ai_integration (
    integration_id SERIAL PRIMARY KEY,
    entity_id INTEGER NOT NULL COMMENT 'معرف الكيان (مشتل، مزرعة، قطعة أرض، إلخ)',
    entity_type VARCHAR(50) NOT NULL COMMENT 'نوع الكيان',
    ai_system_id VARCHAR(100) NOT NULL COMMENT 'معرف في نظام الذكاء الاصطناعي',
    integration_type VARCHAR(50) NOT NULL COMMENT 'نوع التكامل: تشخيص أمراض، تحليل تربة، إلخ',
    last_sync_date TIMESTAMP,
    sync_frequency VARCHAR(20) COMMENT 'تواتر المزامنة: يومي، أسبوعي، إلخ',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    configuration JSON COMMENT 'إعدادات التكامل',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول سجل تشخيص الأمراض
CREATE TABLE IF NOT EXISTS disease_diagnosis_log (
    diagnosis_id SERIAL PRIMARY KEY,
    integration_id INTEGER NOT NULL REFERENCES ai_integration(integration_id),
    entity_id INTEGER NOT NULL COMMENT 'معرف الكيان (مشتل، مزرعة، قطعة أرض، إلخ)',
    entity_type VARCHAR(50) NOT NULL COMMENT 'نوع الكيان',
    diagnosis_date TIMESTAMP NOT NULL,
    disease_detected VARCHAR(100),
    confidence_level DECIMAL(5, 2) COMMENT 'مستوى الثقة في التشخيص',
    affected_area DECIMAL(10, 2) COMMENT 'المساحة المتأثرة',
    severity VARCHAR(20) COMMENT 'شدة الإصابة: منخفضة، متوسطة، عالية',
    image_url VARCHAR(255) COMMENT 'رابط صورة الإصابة',
    recommended_treatment TEXT,
    treatment_applied BOOLEAN DEFAULT FALSE,
    treatment_date TIMESTAMP,
    treatment_result VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول سجل تحليل التربة
CREATE TABLE IF NOT EXISTS soil_analysis_log (
    analysis_id SERIAL PRIMARY KEY,
    integration_id INTEGER NOT NULL REFERENCES ai_integration(integration_id),
    entity_id INTEGER NOT NULL COMMENT 'معرف الكيان (مزرعة، قطعة أرض)',
    entity_type VARCHAR(50) NOT NULL COMMENT 'نوع الكيان',
    analysis_date TIMESTAMP NOT NULL,
    ph_level DECIMAL(4, 2),
    nitrogen_level DECIMAL(6, 2),
    phosphorus_level DECIMAL(6, 2),
    potassium_level DECIMAL(6, 2),
    organic_matter DECIMAL(5, 2),
    texture VARCHAR(50),
    moisture_content DECIMAL(5, 2),
    other_minerals JSON,
    recommendations TEXT,
    actions_taken TEXT,
    action_date TIMESTAMP,
    result VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إنشاء الفهارس لتحسين الأداء
CREATE INDEX idx_nursery_inventory_nursery_id ON nursery_inventory(nursery_id);
CREATE INDEX idx_nursery_inventory_plant_type_id ON nursery_inventory(plant_type_id);
CREATE INDEX idx_farm_plantings_farm_id ON farm_plantings(farm_id);
CREATE INDEX idx_farm_plantings_plot_id ON farm_plantings(plot_id);
CREATE INDEX idx_farm_plantings_crop_id ON farm_plantings(crop_id);
CREATE INDEX idx_agricultural_activities_planting_id ON agricultural_activities(planting_id);
CREATE INDEX idx_agricultural_activities_inventory_id ON agricultural_activities(inventory_id);
CREATE INDEX idx_supply_movements_supply_id ON supply_movements(supply_id);
CREATE INDEX idx_ai_integration_entity ON ai_integration(entity_id, entity_type);
CREATE INDEX idx_disease_diagnosis_integration_id ON disease_diagnosis_log(integration_id);
CREATE INDEX idx_soil_analysis_integration_id ON soil_analysis_log(integration_id);
