"""
Agricultural API - مسارات الزراعة
Gaara ERP v12

API endpoints for agricultural module operations.

@author Global v35.0 Singularity
@version 2.0.0
"""

from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from typing import List, Dict, Any

agricultural_api = Blueprint('agricultural_api', __name__, url_prefix='/api/agricultural')

# ============================================
# Mock Data
# ============================================

MOCK_FARMS = [
    {
        'id': 'FRM001',
        'name': 'مزرعة الواحة',
        'location': 'طريق الإسماعيلية',
        'area': 150,
        'area_unit': 'فدان',
        'type': 'greenhouse',
        'status': 'active',
        'manager': 'أحمد محمد',
        'crops': ['طماطم', 'خيار', 'فلفل'],
        'created_at': '2024-01-01'
    },
    {
        'id': 'FRM002',
        'name': 'مزرعة الفردوس',
        'location': 'وادي النطرون',
        'area': 500,
        'area_unit': 'فدان',
        'type': 'open_field',
        'status': 'active',
        'manager': 'خالد سعيد',
        'crops': ['قمح', 'ذرة', 'برسيم'],
        'created_at': '2023-06-15'
    },
]

MOCK_CROPS = [
    {
        'id': 'CRP001',
        'name': 'طماطم هجين 82',
        'category': 'خضروات',
        'variety': 'هجين',
        'season': 'صيفي',
        'growth_period': 120,
        'yield_estimate': 40,
        'yield_unit': 'طن/فدان'
    },
    {
        'id': 'CRP002',
        'name': 'قمح جيزة 171',
        'category': 'حبوب',
        'variety': 'محسن',
        'season': 'شتوي',
        'growth_period': 150,
        'yield_estimate': 2.5,
        'yield_unit': 'طن/فدان'
    },
]

MOCK_DIAGNOSES = [
    {
        'id': 'DGN001',
        'crop': 'طماطم',
        'farm': 'مزرعة الواحة',
        'farm_id': 'FRM001',
        'symptoms': 'بقع صفراء على الأوراق مع ذبول تدريجي',
        'disease': 'اللفحة المتأخرة',
        'disease_en': 'Late Blight',
        'severity': 'high',
        'status': 'treating',
        'diagnosis_date': '2026-01-15',
        'confidence': 92,
        'treatment': 'مبيد فطري نحاسي'
    },
]

MOCK_EXPERIMENTS = [
    {
        'id': 'EXP001',
        'title': 'تقييم أصناف الطماطم الجديدة',
        'code': 'VT-2026-001',
        'type': 'variety_trial',
        'crop': 'طماطم',
        'status': 'active',
        'progress': 45,
        'researcher': 'د. أحمد محمد',
        'start_date': '2026-01-01'
    },
]

MOCK_HYBRIDIZATIONS = [
    {
        'id': 'HYB001',
        'code': 'TOM-HY-2026-001',
        'parent_female': 'طماطم سوبر سترين',
        'parent_male': 'طماطم هجين 82',
        'crop': 'طماطم',
        'status': 'evaluating',
        'f1_seeds': 150,
        'germination_rate': 85,
        'cross_date': '2026-01-05',
        'breeder': 'د. أحمد محمد'
    },
]


# ============================================
# Farm Endpoints
# ============================================

@agricultural_api.route('/farms', methods=['GET'])
def get_farms() -> Response:
    """Get all farms"""
    return jsonify({
        'success': True,
        'data': MOCK_FARMS,
        'total': len(MOCK_FARMS)
    })


@agricultural_api.route('/farms/<farm_id>', methods=['GET'])
def get_farm(farm_id: str) -> Response:
    """Get farm by ID"""
    farm = next((f for f in MOCK_FARMS if f['id'] == farm_id), None)
    if not farm:
        return jsonify({'success': False, 'message_ar': 'المزرعة غير موجودة'}), 404
    return jsonify({'success': True, 'data': farm})


@agricultural_api.route('/farms', methods=['POST'])
def create_farm() -> Response:
    """Create new farm"""
    data = request.get_json()
    new_id = f"FRM{len(MOCK_FARMS) + 1:03d}"
    new_farm = {
        'id': new_id,
        'name': data.get('name', ''),
        'location': data.get('location', ''),
        'area': data.get('area', 0),
        'area_unit': data.get('area_unit', 'فدان'),
        'type': data.get('type', 'open_field'),
        'status': 'active',
        'manager': data.get('manager', ''),
        'crops': data.get('crops', []),
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    MOCK_FARMS.append(new_farm)
    return jsonify({
        'success': True,
        'data': new_farm,
        'message_ar': 'تم إضافة المزرعة بنجاح'
    }), 201


@agricultural_api.route('/farms/<farm_id>', methods=['PUT'])
def update_farm(farm_id: str) -> Response:
    """Update farm"""
    data = request.get_json()
    farm = next((f for f in MOCK_FARMS if f['id'] == farm_id), None)
    if not farm:
        return jsonify({'success': False, 'message_ar': 'المزرعة غير موجودة'}), 404
    
    farm.update({
        'name': data.get('name', farm['name']),
        'location': data.get('location', farm['location']),
        'area': data.get('area', farm['area']),
        'type': data.get('type', farm['type']),
        'manager': data.get('manager', farm['manager']),
    })
    return jsonify({'success': True, 'data': farm, 'message_ar': 'تم تحديث المزرعة'})


@agricultural_api.route('/farms/<farm_id>', methods=['DELETE'])
def delete_farm(farm_id: str) -> Response:
    """Delete farm"""
    global MOCK_FARMS
    MOCK_FARMS = [f for f in MOCK_FARMS if f['id'] != farm_id]
    return jsonify({'success': True, 'message_ar': 'تم حذف المزرعة'})


# ============================================
# Crop Endpoints
# ============================================

@agricultural_api.route('/crops', methods=['GET'])
def get_crops() -> Response:
    """Get all crops"""
    return jsonify({
        'success': True,
        'data': MOCK_CROPS,
        'total': len(MOCK_CROPS)
    })


@agricultural_api.route('/crops/<crop_id>', methods=['GET'])
def get_crop(crop_id: str) -> Response:
    """Get crop by ID"""
    crop = next((c for c in MOCK_CROPS if c['id'] == crop_id), None)
    if not crop:
        return jsonify({'success': False, 'message_ar': 'المحصول غير موجود'}), 404
    return jsonify({'success': True, 'data': crop})


@agricultural_api.route('/crops', methods=['POST'])
def create_crop() -> Response:
    """Create new crop"""
    data = request.get_json()
    new_id = f"CRP{len(MOCK_CROPS) + 1:03d}"
    new_crop = {
        'id': new_id,
        'name': data.get('name', ''),
        'category': data.get('category', ''),
        'variety': data.get('variety', ''),
        'season': data.get('season', ''),
        'growth_period': data.get('growth_period', 0),
        'yield_estimate': data.get('yield_estimate', 0),
        'yield_unit': data.get('yield_unit', 'طن/فدان')
    }
    MOCK_CROPS.append(new_crop)
    return jsonify({
        'success': True,
        'data': new_crop,
        'message_ar': 'تم إضافة المحصول بنجاح'
    }), 201


# ============================================
# Diagnosis Endpoints
# ============================================

@agricultural_api.route('/diagnoses', methods=['GET'])
def get_diagnoses() -> Response:
    """Get all diagnoses"""
    status = request.args.get('status')
    severity = request.args.get('severity')
    
    filtered = MOCK_DIAGNOSES
    if status:
        filtered = [d for d in filtered if d['status'] == status]
    if severity:
        filtered = [d for d in filtered if d['severity'] == severity]
    
    return jsonify({
        'success': True,
        'data': filtered,
        'total': len(filtered)
    })


@agricultural_api.route('/diagnoses/<diagnosis_id>', methods=['GET'])
def get_diagnosis(diagnosis_id: str) -> Response:
    """Get diagnosis by ID"""
    diagnosis = next((d for d in MOCK_DIAGNOSES if d['id'] == diagnosis_id), None)
    if not diagnosis:
        return jsonify({'success': False, 'message_ar': 'التشخيص غير موجود'}), 404
    return jsonify({'success': True, 'data': diagnosis})


@agricultural_api.route('/diagnoses', methods=['POST'])
def create_diagnosis() -> Response:
    """Create new diagnosis case"""
    data = request.get_json()
    new_id = f"DGN{len(MOCK_DIAGNOSES) + 1:03d}"
    new_diagnosis = {
        'id': new_id,
        'crop': data.get('crop', ''),
        'farm': data.get('farm', ''),
        'farm_id': data.get('farm_id', ''),
        'symptoms': data.get('symptoms', ''),
        'disease': None,
        'disease_en': None,
        'severity': data.get('severity', 'medium'),
        'status': 'pending',
        'diagnosis_date': datetime.now().strftime('%Y-%m-%d'),
        'confidence': 0,
        'treatment': None
    }
    MOCK_DIAGNOSES.append(new_diagnosis)
    return jsonify({
        'success': True,
        'data': new_diagnosis,
        'message_ar': 'تم إرسال الحالة للتشخيص'
    }), 201


@agricultural_api.route('/diagnoses/<diagnosis_id>/ai-diagnose', methods=['POST'])
def ai_diagnose(diagnosis_id: str) -> Response:
    """Run AI diagnosis"""
    diagnosis = next((d for d in MOCK_DIAGNOSES if d['id'] == diagnosis_id), None)
    if not diagnosis:
        return jsonify({'success': False, 'message_ar': 'التشخيص غير موجود'}), 404
    
    # Simulate AI diagnosis
    import random
    diseases = [
        ('اللفحة المتأخرة', 'Late Blight'),
        ('البياض الدقيقي', 'Powdery Mildew'),
        ('الذبول الفيوزاريومي', 'Fusarium Wilt'),
    ]
    disease = random.choice(diseases)
    
    diagnosis['disease'] = disease[0]
    diagnosis['disease_en'] = disease[1]
    diagnosis['status'] = 'diagnosed'
    diagnosis['confidence'] = random.randint(85, 98)
    
    return jsonify({
        'success': True,
        'data': diagnosis,
        'message_ar': 'تم التشخيص بنجاح'
    })


@agricultural_api.route('/diagnoses/<diagnosis_id>/treatment', methods=['POST'])
def add_treatment(diagnosis_id: str) -> Response:
    """Add treatment to diagnosis"""
    data = request.get_json()
    diagnosis = next((d for d in MOCK_DIAGNOSES if d['id'] == diagnosis_id), None)
    if not diagnosis:
        return jsonify({'success': False, 'message_ar': 'التشخيص غير موجود'}), 404
    
    diagnosis['treatment'] = data.get('product', '')
    diagnosis['status'] = 'treating'
    
    return jsonify({
        'success': True,
        'data': diagnosis,
        'message_ar': 'تم إضافة العلاج'
    })


# ============================================
# Experiment Endpoints
# ============================================

@agricultural_api.route('/experiments', methods=['GET'])
def get_experiments() -> Response:
    """Get all experiments"""
    return jsonify({
        'success': True,
        'data': MOCK_EXPERIMENTS,
        'total': len(MOCK_EXPERIMENTS)
    })


@agricultural_api.route('/experiments', methods=['POST'])
def create_experiment() -> Response:
    """Create new experiment"""
    data = request.get_json()
    new_id = f"EXP{len(MOCK_EXPERIMENTS) + 1:03d}"
    new_experiment = {
        'id': new_id,
        'title': data.get('title', ''),
        'code': data.get('code', ''),
        'type': data.get('type', 'variety_trial'),
        'crop': data.get('crop', ''),
        'status': 'planning',
        'progress': 0,
        'researcher': data.get('researcher', ''),
        'start_date': data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    }
    MOCK_EXPERIMENTS.append(new_experiment)
    return jsonify({
        'success': True,
        'data': new_experiment,
        'message_ar': 'تم إنشاء التجربة بنجاح'
    }), 201


@agricultural_api.route('/experiments/<exp_id>/status', methods=['PUT'])
def update_experiment_status(exp_id: str) -> Response:
    """Update experiment status"""
    data = request.get_json()
    experiment = next((e for e in MOCK_EXPERIMENTS if e['id'] == exp_id), None)
    if not experiment:
        return jsonify({'success': False, 'message_ar': 'التجربة غير موجودة'}), 404
    
    experiment['status'] = data.get('status', experiment['status'])
    if experiment['status'] == 'completed':
        experiment['progress'] = 100
    
    return jsonify({
        'success': True,
        'data': experiment,
        'message_ar': 'تم تحديث حالة التجربة'
    })


# ============================================
# Hybridization Endpoints
# ============================================

@agricultural_api.route('/hybridizations', methods=['GET'])
def get_hybridizations() -> Response:
    """Get all hybridization crosses"""
    return jsonify({
        'success': True,
        'data': MOCK_HYBRIDIZATIONS,
        'total': len(MOCK_HYBRIDIZATIONS)
    })


@agricultural_api.route('/hybridizations', methods=['POST'])
def create_hybridization() -> Response:
    """Create new hybridization cross"""
    data = request.get_json()
    new_id = f"HYB{len(MOCK_HYBRIDIZATIONS) + 1:03d}"
    crop_prefix = {'طماطم': 'TOM', 'قمح': 'WHT', 'خيار': 'CUC'}.get(data.get('crop', ''), 'CRP')
    
    new_cross = {
        'id': new_id,
        'code': data.get('code', f"{crop_prefix}-HY-{datetime.now().year}-{len(MOCK_HYBRIDIZATIONS) + 1:03d}"),
        'parent_female': data.get('parent_female', ''),
        'parent_male': data.get('parent_male', ''),
        'crop': data.get('crop', ''),
        'status': 'planned',
        'f1_seeds': 0,
        'germination_rate': 0,
        'cross_date': data.get('cross_date', datetime.now().strftime('%Y-%m-%d')),
        'breeder': data.get('breeder', '')
    }
    MOCK_HYBRIDIZATIONS.append(new_cross)
    return jsonify({
        'success': True,
        'data': new_cross,
        'message_ar': 'تم إنشاء التهجين بنجاح'
    }), 201


@agricultural_api.route('/hybridizations/<hyb_id>/status', methods=['PUT'])
def update_hybridization_status(hyb_id: str) -> Response:
    """Update hybridization status"""
    data = request.get_json()
    cross = next((h for h in MOCK_HYBRIDIZATIONS if h['id'] == hyb_id), None)
    if not cross:
        return jsonify({'success': False, 'message_ar': 'التهجين غير موجود'}), 404
    
    cross['status'] = data.get('status', cross['status'])
    
    return jsonify({
        'success': True,
        'data': cross,
        'message_ar': 'تم تحديث حالة التهجين'
    })


# ============================================
# Statistics Endpoints
# ============================================

@agricultural_api.route('/stats', methods=['GET'])
def get_stats() -> Response:
    """Get agricultural statistics"""
    return jsonify({
        'success': True,
        'data': {
            'total_farms': len(MOCK_FARMS),
            'active_farms': len([f for f in MOCK_FARMS if f['status'] == 'active']),
            'total_area': sum(f['area'] for f in MOCK_FARMS),
            'total_crops': len(MOCK_CROPS),
            'active_diagnoses': len([d for d in MOCK_DIAGNOSES if d['status'] not in ['resolved']]),
            'active_experiments': len([e for e in MOCK_EXPERIMENTS if e['status'] == 'active']),
            'active_hybridizations': len([h for h in MOCK_HYBRIDIZATIONS if h['status'] not in ['selected', 'rejected']]),
        }
    })
