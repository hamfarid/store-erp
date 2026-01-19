# دليل المطور - نظام Gaara AI

## 📋 جدول المحتويات

1. [نظرة عامة على البنية](#نظرة-عامة-على-البنية)
2. [إعداد بيئة التطوير](#إعداد-بيئة-التطوير)
3. [هيكل المشروع](#هيكل-المشروع)
4. [الواجهة الخلفية (Backend)](#الواجهة-الخلفية-backend)
5. [الواجهة الأمامية (Frontend)](#الواجهة-الأمامية-frontend)
6. [قاعدة البيانات](#قاعدة-البيانات)
7. [الذكاء الاصطناعي](#الذكاء-الاصطناعي)
8. [APIs والتوثيق](#apis-والتوثيق)
9. [الاختبارات](#الاختبارات)
10. [النشر](#النشر)
11. [أفضل الممارسات](#أفضل-الممارسات)

## نظرة عامة على البنية

نظام Gaara AI مبني على معمارية حديثة تفصل بين الواجهة الأمامية والخلفية:

### المكونات الرئيسية

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  Flask Backend  │    │   AI Engine     │
│                 │◄──►│                 │◄──►│                 │
│  - UI Components│    │  - REST APIs    │    │  - TensorFlow   │
│  - State Mgmt   │    │  - Business     │    │  - OpenCV       │
│  - Routing      │    │    Logic        │    │  - Image Proc   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │                 │
                       │  - Users        │
                       │  - Farms        │
                       │  - Diseases     │
                       │  - Diagnoses    │
                       └─────────────────┘
```

### التقنيات المستخدمة

| المكون | التقنية | الإصدار | الغرض |
|--------|---------|---------|--------|
| Frontend | React | 18.2+ | واجهة المستخدم |
| Build Tool | Vite | 4.0+ | بناء وتطوير Frontend |
| Styling | Tailwind CSS | 3.0+ | تصميم الواجهة |
| Charts | Recharts | 2.5+ | الرسوم البيانية |
| Backend | Flask | 2.3+ | خادم API |
| Database | SQLAlchemy | 2.0+ | ORM وقاعدة البيانات |
| AI/ML | TensorFlow | 2.13+ | نماذج الذكاء الاصطناعي |
| Image Processing | OpenCV | 4.8+ | معالجة الصور |

## إعداد بيئة التطوير

### المتطلبات الأساسية

```bash
# Python 3.8+
python --version

# Node.js 16+
node --version
npm --version

# Git
git --version
```

### إعداد البيئة الافتراضية

```bash
# إنشاء بيئة Python
python -m venv gaara_env

# تفعيل البيئة
source gaara_env/bin/activate  # Linux/Mac
gaara_env\Scripts\activate     # Windows

# تحديث pip
pip install --upgrade pip
```

### تثبيت أدوات التطوير

```bash
# أدوات Python للتطوير
pip install black flake8 pytest pytest-cov mypy

# أدوات Node.js للتطوير
npm install -g eslint prettier @typescript-eslint/parser
```

## هيكل المشروع

```
gaara-ai-system/
├── backend/                    # الواجهة الخلفية
│   ├── main_api.py            # التطبيق الرئيسي
│   ├── ai_diagnosis.py        # نظام التشخيص بالذكاء الاصطناعي
│   ├── models/                # نماذج قاعدة البيانات
│   ├── routes/                # مسارات API
│   ├── services/              # خدمات الأعمال
│   ├── utils/                 # أدوات مساعدة
│   ├── tests/                 # اختبارات Backend
│   └── requirements.txt       # متطلبات Python
├── frontend/                  # الواجهة الأمامية
│   ├── src/
│   │   ├── components/        # مكونات React
│   │   ├── pages/            # صفحات التطبيق
│   │   ├── services/         # خدمات API
│   │   ├── hooks/            # React Hooks مخصصة
│   │   ├── utils/            # أدوات مساعدة
│   │   └── styles/           # ملفات CSS
│   ├── public/               # ملفات عامة
│   ├── tests/                # اختبارات Frontend
│   ├── package.json          # متطلبات Node.js
│   └── vite.config.js        # إعدادات Vite
├── docs/                     # التوثيق
├── docker/                   # ملفات Docker
├── scripts/                  # سكريبتات مساعدة
└── README.md                 # الدليل الرئيسي
```

## الواجهة الخلفية (Backend)

### بنية Flask Application

```python
# main_api.py - الهيكل الأساسي
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaara.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# تسجيل المسارات
from routes import auth, farms, diseases, diagnosis
app.register_blueprint(auth.bp)
app.register_blueprint(farms.bp)
app.register_blueprint(diseases.bp)
app.register_blueprint(diagnosis.bp)
```

### نماذج قاعدة البيانات

```python
# models/user.py
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    farms = db.relationship('Farm', backref='owner', lazy=True)
    diagnoses = db.relationship('Diagnosis', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
```

### خدمات الأعمال

```python
# services/farm_service.py
class FarmService:
    @staticmethod
    def create_farm(data, user_id):
        """إنشاء مزرعة جديدة"""
        farm = Farm(
            name=data['name'],
            location=data['location'],
            area=data['area'],
            owner_id=user_id
        )
        db.session.add(farm)
        db.session.commit()
        return farm
    
    @staticmethod
    def get_user_farms(user_id):
        """الحصول على مزارع المستخدم"""
        return Farm.query.filter_by(owner_id=user_id).all()
    
    @staticmethod
    def update_farm(farm_id, data, user_id):
        """تحديث بيانات المزرعة"""
        farm = Farm.query.filter_by(id=farm_id, owner_id=user_id).first()
        if not farm:
            raise ValueError("المزرعة غير موجودة")
        
        for key, value in data.items():
            if hasattr(farm, key):
                setattr(farm, key, value)
        
        db.session.commit()
        return farm
```

### مسارات API

```python
# routes/farms.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.farm_service import FarmService

bp = Blueprint('farms', __name__, url_prefix='/api/farms')

@bp.route('', methods=['GET'])
@jwt_required()
def get_farms():
    """الحصول على قائمة المزارع"""
    user_id = get_jwt_identity()
    farms = FarmService.get_user_farms(user_id)
    return jsonify([farm.to_dict() for farm in farms])

@bp.route('', methods=['POST'])
@jwt_required()
def create_farm():
    """إنشاء مزرعة جديدة"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # التحقق من صحة البيانات
    required_fields = ['name', 'location', 'area']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'الحقل {field} مطلوب'}), 400
    
    try:
        farm = FarmService.create_farm(data, user_id)
        return jsonify(farm.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## الواجهة الأمامية (Frontend)

### بنية React Application

```jsx
// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ToastContainer } from 'react-toastify';

// استيراد الصفحات
import Dashboard from './pages/Dashboard';
import Farms from './pages/Farms';
import Diseases from './pages/Diseases';
import Diagnosis from './pages/Diagnosis';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/farms" element={<Farms />} />
            <Route path="/diseases" element={<Diseases />} />
            <Route path="/diagnosis" element={<Diagnosis />} />
          </Routes>
          <ToastContainer position="top-right" />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
```

### خدمات API

```javascript
// src/services/ApiService.js
class ApiService {
  constructor() {
    this.baseURL = 'http://localhost:5000/api';
    this.token = localStorage.getItem('token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'حدث خطأ في الطلب');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // دوال المزارع
  async getFarms() {
    return this.request('/farms');
  }

  async createFarm(farmData) {
    return this.request('/farms', {
      method: 'POST',
      body: JSON.stringify(farmData),
    });
  }

  async updateFarm(farmId, farmData) {
    return this.request(`/farms/${farmId}`, {
      method: 'PUT',
      body: JSON.stringify(farmData),
    });
  }

  async deleteFarm(farmId) {
    return this.request(`/farms/${farmId}`, {
      method: 'DELETE',
    });
  }
}

export default new ApiService();
```

### مكونات React

```jsx
// src/components/FarmCard.jsx
import React from 'react';
import { MapPinIcon, ChartBarIcon } from '@heroicons/react/24/outline';

const FarmCard = ({ farm, onEdit, onDelete, onViewDetails }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold text-gray-900">{farm.name}</h3>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(farm)}
            className="text-blue-600 hover:text-blue-800"
          >
            تعديل
          </button>
          <button
            onClick={() => onDelete(farm.id)}
            className="text-red-600 hover:text-red-800"
          >
            حذف
          </button>
        </div>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-center text-gray-600">
          <MapPinIcon className="h-5 w-5 ml-2" />
          <span>{farm.location}</span>
        </div>
        
        <div className="flex items-center text-gray-600">
          <ChartBarIcon className="h-5 w-5 ml-2" />
          <span>{farm.area} هكتار</span>
        </div>
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <button
          onClick={() => onViewDetails(farm)}
          className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition-colors"
        >
          عرض التفاصيل
        </button>
      </div>
    </div>
  );
};

export default FarmCard;
```

### إدارة الحالة

```jsx
// src/contexts/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      loadUser();
    } else {
      setLoading(false);
    }
  }, []);

  const loadUser = async () => {
    try {
      const userData = await ApiService.getProfile();
      setUser(userData);
    } catch (error) {
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const response = await ApiService.login(email, password);
    localStorage.setItem('token', response.token);
    setUser(response.user);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

## قاعدة البيانات

### تصميم قاعدة البيانات

```sql
-- جدول المستخدمين
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- جدول المزارع
CREATE TABLE farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    owner_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- جدول المحاصيل
CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    variety VARCHAR(100),
    planting_date DATE,
    expected_harvest DATE,
    farm_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

-- جدول الأمراض
CREATE TABLE diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(150),
    description TEXT,
    symptoms TEXT,
    treatment TEXT,
    prevention TEXT,
    severity VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- جدول التشخيصات
CREATE TABLE diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path VARCHAR(255),
    disease_id INTEGER,
    confidence DECIMAL(5,2),
    plant_type VARCHAR(100),
    user_id INTEGER NOT NULL,
    farm_id INTEGER,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disease_id) REFERENCES diseases(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);
```

### الفهارس والتحسينات

```sql
-- فهارس لتحسين الأداء
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_farms_owner ON farms(owner_id);
CREATE INDEX idx_crops_farm ON crops(farm_id);
CREATE INDEX idx_diagnoses_user ON diagnoses(user_id);
CREATE INDEX idx_diagnoses_date ON diagnoses(created_at);
CREATE INDEX idx_diagnoses_disease ON diagnoses(disease_id);
```

## الذكاء الاصطناعي

### نموذج تشخيص الأمراض

```python
# ai_diagnosis.py - النموذج الأساسي
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2

class PlantDiseaseModel:
    def __init__(self, num_classes=10):
        self.num_classes = num_classes
        self.model = self._build_model()
        self.image_size = (224, 224)
    
    def _build_model(self):
        """بناء نموذج CNN لتصنيف أمراض النباتات"""
        model = models.Sequential([
            # طبقات التحويل
            layers.Conv2D(32, (3, 3), activation='relu', 
                         input_shape=(224, 224, 3)),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            # طبقات التصنيف
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(512, activation='relu'),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_image(self, image_path):
        """معالجة الصورة قبل التنبؤ"""
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, self.image_size)
        image = image.astype('float32') / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    
    def predict(self, image_path):
        """التنبؤ بالمرض من الصورة"""
        processed_image = self.preprocess_image(image_path)
        predictions = self.model.predict(processed_image)
        
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'all_predictions': predictions[0].tolist()
        }
```

### تدريب النموذج

```python
# training/train_model.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os

class ModelTrainer:
    def __init__(self, data_dir, model_save_path):
        self.data_dir = data_dir
        self.model_save_path = model_save_path
        self.batch_size = 32
        self.epochs = 50
        self.image_size = (224, 224)
    
    def prepare_data(self):
        """تحضير البيانات للتدريب"""
        # مولد البيانات مع التحسينات
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            validation_split=0.2
        )
        
        # بيانات التدريب
        train_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )
        
        # بيانات التحقق
        validation_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.image_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )
        
        return train_generator, validation_generator
    
    def train_model(self):
        """تدريب النموذج"""
        train_gen, val_gen = self.prepare_data()
        
        # إنشاء النموذج
        model = PlantDiseaseModel(num_classes=len(train_gen.class_indices))
        
        # callbacks للتحسين
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                patience=10, restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                factor=0.2, patience=5, min_lr=0.001
            ),
            tf.keras.callbacks.ModelCheckpoint(
                self.model_save_path, save_best_only=True
            )
        ]
        
        # التدريب
        history = model.model.fit(
            train_gen,
            epochs=self.epochs,
            validation_data=val_gen,
            callbacks=callbacks
        )
        
        return model, history
```

## APIs والتوثيق

### توثيق API باستخدام Swagger

```python
# api_docs.py
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_restx import Namespace

# إعداد Swagger
api = Api(
    title='Gaara AI API',
    version='2.0',
    description='API للنظام الزراعي الذكي',
    doc='/api/docs/'
)

# تعريف النماذج
farm_model = api.model('Farm', {
    'id': fields.Integer(description='معرف المزرعة'),
    'name': fields.String(required=True, description='اسم المزرعة'),
    'location': fields.String(required=True, description='موقع المزرعة'),
    'area': fields.Float(required=True, description='مساحة المزرعة بالهكتار'),
    'owner_id': fields.Integer(description='معرف المالك')
})

diagnosis_model = api.model('Diagnosis', {
    'image': fields.String(required=True, description='صورة النبات (base64)'),
    'plant_type': fields.String(description='نوع النبات'),
    'farm_id': fields.Integer(description='معرف المزرعة')
})

# مساحة أسماء للمزارع
farms_ns = Namespace('farms', description='عمليات المزارع')

@farms_ns.route('/')
class FarmList(Resource):
    @farms_ns.doc('list_farms')
    @farms_ns.marshal_list_with(farm_model)
    def get(self):
        """الحصول على قائمة المزارع"""
        pass
    
    @farms_ns.doc('create_farm')
    @farms_ns.expect(farm_model)
    @farms_ns.marshal_with(farm_model, code=201)
    def post(self):
        """إنشاء مزرعة جديدة"""
        pass

@farms_ns.route('/<int:farm_id>')
class Farm(Resource):
    @farms_ns.doc('get_farm')
    @farms_ns.marshal_with(farm_model)
    def get(self, farm_id):
        """الحصول على مزرعة محددة"""
        pass
    
    @farms_ns.doc('update_farm')
    @farms_ns.expect(farm_model)
    @farms_ns.marshal_with(farm_model)
    def put(self, farm_id):
        """تحديث بيانات المزرعة"""
        pass
    
    @farms_ns.doc('delete_farm')
    def delete(self, farm_id):
        """حذف المزرعة"""
        pass

api.add_namespace(farms_ns, path='/api/farms')
```

### أمثلة على استخدام API

```bash
# تسجيل الدخول
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# إنشاء مزرعة جديدة
curl -X POST http://localhost:5000/api/farms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "مزرعة الورود",
    "location": "الرياض",
    "area": 15.5
  }'

# تشخيص مرض النبات
curl -X POST http://localhost:5000/api/diagnosis \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "plant_type": "طماطم",
    "farm_id": 1
  }'
```

## الاختبارات

### اختبارات Backend

```python
# tests/test_farms.py
import pytest
from main_api import app, db
from models.user import User
from models.farm import Farm

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth_headers(client):
    # إنشاء مستخدم للاختبار
    user = User(name='Test User', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    # تسجيل الدخول
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

def test_create_farm(client, auth_headers):
    """اختبار إنشاء مزرعة جديدة"""
    farm_data = {
        'name': 'مزرعة الاختبار',
        'location': 'الرياض',
        'area': 10.5
    }
    
    response = client.post('/api/farms', 
                          json=farm_data, 
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == farm_data['name']
    assert data['location'] == farm_data['location']

def test_get_farms(client, auth_headers):
    """اختبار الحصول على قائمة المزارع"""
    response = client.get('/api/farms', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
```

### اختبارات Frontend

```javascript
// tests/components/FarmCard.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FarmCard from '../src/components/FarmCard';

const mockFarm = {
  id: 1,
  name: 'مزرعة الاختبار',
  location: 'الرياض',
  area: 10.5
};

const mockHandlers = {
  onEdit: jest.fn(),
  onDelete: jest.fn(),
  onViewDetails: jest.fn()
};

describe('FarmCard Component', () => {
  test('renders farm information correctly', () => {
    render(<FarmCard farm={mockFarm} {...mockHandlers} />);
    
    expect(screen.getByText('مزرعة الاختبار')).toBeInTheDocument();
    expect(screen.getByText('الرياض')).toBeInTheDocument();
    expect(screen.getByText('10.5 هكتار')).toBeInTheDocument();
  });

  test('calls onEdit when edit button is clicked', () => {
    render(<FarmCard farm={mockFarm} {...mockHandlers} />);
    
    const editButton = screen.getByText('تعديل');
    fireEvent.click(editButton);
    
    expect(mockHandlers.onEdit).toHaveBeenCalledWith(mockFarm);
  });

  test('calls onDelete when delete button is clicked', () => {
    render(<FarmCard farm={mockFarm} {...mockHandlers} />);
    
    const deleteButton = screen.getByText('حذف');
    fireEvent.click(deleteButton);
    
    expect(mockHandlers.onDelete).toHaveBeenCalledWith(mockFarm.id);
  });
});
```

## النشر

### Docker Configuration

```dockerfile
# Dockerfile.backend
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main_api.py"]
```

```dockerfile
# Dockerfile.frontend
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///gaara_prod.db
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
```

## أفضل الممارسات

### أمان التطبيق

```python
# security/auth.py
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def require_role(required_role):
    """decorator للتحقق من صلاحيات المستخدم"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or user.role != required_role:
                return jsonify({'error': 'غير مصرح لك بهذا الإجراء'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# استخدام decorator
@app.route('/api/admin/users')
@require_role('admin')
def get_all_users():
    """الحصول على جميع المستخدمين - للمديرين فقط"""
    pass
```

### تحسين الأداء

```python
# performance/caching.py
from flask_caching import Cache
import redis

# إعداد Redis للتخزين المؤقت
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@app.route('/api/diseases')
@cache.cached(timeout=3600)  # تخزين مؤقت لساعة واحدة
def get_diseases():
    """الحصول على قائمة الأمراض مع تخزين مؤقت"""
    diseases = Disease.query.all()
    return jsonify([disease.to_dict() for disease in diseases])
```

### معالجة الأخطاء

```python
# error_handling.py
from flask import jsonify
import logging

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'المورد غير موجود'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logging.error(f'خطأ خادم: {str(error)}')
    return jsonify({'error': 'خطأ داخلي في الخادم'}), 500

@app.errorhandler(ValidationError)
def validation_error(error):
    return jsonify({'error': str(error)}), 400
```

### مراقبة الأداء

```python
# monitoring/metrics.py
from prometheus_flask_exporter import PrometheusMetrics
import time

# إعداد Prometheus
metrics = PrometheusMetrics(app)

# مقاييس مخصصة
diagnosis_counter = metrics.counter(
    'diagnoses_total', 
    'إجمالي عدد التشخيصات',
    labels={'plant_type': lambda: request.json.get('plant_type', 'unknown')}
)

@app.route('/api/diagnosis', methods=['POST'])
@diagnosis_counter
def diagnose():
    """تشخيص مرض النبات مع مراقبة الأداء"""
    start_time = time.time()
    
    try:
        # منطق التشخيص
        result = perform_diagnosis(request.json)
        
        # تسجيل وقت الاستجابة
        response_time = time.time() - start_time
        metrics.histogram(
            'diagnosis_duration_seconds',
            'مدة التشخيص بالثواني'
        ).observe(response_time)
        
        return jsonify(result)
    
    except Exception as e:
        metrics.counter(
            'diagnosis_errors_total',
            'إجمالي أخطاء التشخيص'
        ).inc()
        raise
```

---

**تم إعداد هذا الدليل بواسطة**: Manus AI  
**آخر تحديث**: ديسمبر 2024  
**الإصدار**: 2.0.0

