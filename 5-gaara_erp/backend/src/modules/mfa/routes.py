# -*- coding: utf-8 -*-
"""
مسارات المصادقة الثنائية
MFA Routes

API endpoints للمصادقة الثنائية
API endpoints for Multi-Factor Authentication
"""

from flask import Blueprint, request, jsonify
import logging

try:
    from flask_jwt_extended import jwt_required, get_jwt_identity
except ImportError:
    # Fallback for testing
    def jwt_required():
        def decorator(f):
            return f
        return decorator
    
    def get_jwt_identity():
        return 1

from .service import MFAService

try:
    from src.database import db
    from src.models.user import User
except ImportError:
    db = None
    User = None

logger = logging.getLogger(__name__)

mfa_bp = Blueprint('mfa', __name__, url_prefix='/api/auth/mfa')


@mfa_bp.route('/setup', methods=['POST'])
@jwt_required()
def setup_mfa():
    """
    إعداد المصادقة الثنائية
    Setup MFA for current user.
    
    Request Body:
        device_name: Optional name for the device
        
    Returns:
        QR code and device info for authenticator app setup
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        device_name = data.get('device_name', 'Primary Device')
        
        # Check if MFA already enabled
        if MFAService.is_mfa_enabled(user_id):
            return jsonify({
                'success': False,
                'message': 'المصادقة الثنائية مفعلة بالفعل',
                'message_en': 'MFA is already enabled'
            }), 400
        
        # Create device
        device, _ = MFAService.setup_mfa(user_id, device_name)
        
        # Get user email for QR code
        user = User.query.get(user_id) if User else None
        email = user.email if user else f'user_{user_id}@gaara.erp'
        
        # Generate QR code
        qr_base64 = MFAService.generate_qr_code(device, email)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'device_id': device.id,
                'device_name': device.name,
                'secret': device.secret,  # For manual entry
                'qr_code': f'data:image/png;base64,{qr_base64}',
            },
            'message': 'امسح رمز QR باستخدام تطبيق المصادقة',
            'message_en': 'Scan QR code with your authenticator app'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"MFA setup error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء إعداد المصادقة الثنائية',
            'message_en': 'Error setting up MFA'
        }), 500


@mfa_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_mfa():
    """
    التحقق من رمز المصادقة وتفعيل الجهاز
    Verify TOTP token and activate MFA device.
    
    Request Body:
        device_id: MFA device ID
        token: 6-digit TOTP code
        
    Returns:
        Backup codes (only shown once!)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'البيانات مطلوبة',
                'message_en': 'Request body required'
            }), 400
        
        device_id = data.get('device_id')
        token = data.get('token')
        
        if not device_id or not token:
            return jsonify({
                'success': False,
                'message': 'معرف الجهاز والرمز مطلوبان',
                'message_en': 'Device ID and token required'
            }), 400
        
        # Verify and activate
        if MFAService.verify_and_activate(device_id, user_id, token):
            # Get backup codes count
            remaining = MFAService.get_backup_codes_count(user_id)
            
            return jsonify({
                'success': True,
                'data': {
                    'mfa_enabled': True,
                    'backup_codes_count': remaining,
                },
                'message': 'تم تفعيل المصادقة الثنائية بنجاح',
                'message_en': 'MFA enabled successfully'
            })
        
        return jsonify({
            'success': False,
            'message': 'رمز غير صالح',
            'message_en': 'Invalid token'
        }), 400
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"MFA verify error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء التحقق',
            'message_en': 'Verification error'
        }), 500


@mfa_bp.route('/validate', methods=['POST'])
def validate_mfa():
    """
    التحقق من رمز المصادقة عند تسجيل الدخول
    Validate MFA token during login.
    
    Request Body:
        user_id: User ID (from initial login step)
        token: 6-digit TOTP code
        
    Returns:
        Validation result
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'البيانات مطلوبة'
            }), 400
        
        user_id = data.get('user_id')
        token = data.get('token')
        
        if not user_id or not token:
            return jsonify({
                'success': False,
                'message': 'معرف المستخدم والرمز مطلوبان'
            }), 400
        
        if MFAService.verify_token(user_id, token):
            return jsonify({
                'success': True,
                'data': {'verified': True},
                'message': 'تم التحقق بنجاح'
            })
        
        return jsonify({
            'success': False,
            'message': 'رمز غير صالح'
        }), 400
        
    except Exception as e:
        logger.error(f"MFA validate error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء التحقق'
        }), 500


@mfa_bp.route('/backup-code', methods=['POST'])
def verify_backup_code():
    """
    التحقق من رمز النسخ الاحتياطي
    Verify backup code during login.
    
    Request Body:
        user_id: User ID
        code: 8-character backup code
        
    Returns:
        Validation result
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'البيانات مطلوبة'
            }), 400
        
        user_id = data.get('user_id')
        code = data.get('code')
        
        if not user_id or not code:
            return jsonify({
                'success': False,
                'message': 'معرف المستخدم والرمز مطلوبان'
            }), 400
        
        if MFAService.verify_backup_code(user_id, code):
            remaining = MFAService.get_backup_codes_count(user_id)
            
            return jsonify({
                'success': True,
                'data': {
                    'verified': True,
                    'remaining_codes': remaining
                },
                'message': f'تم التحقق. متبقي {remaining} رموز احتياطية'
            })
        
        return jsonify({
            'success': False,
            'message': 'رمز النسخ الاحتياطي غير صالح'
        }), 400
        
    except Exception as e:
        logger.error(f"Backup code verify error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء التحقق'
        }), 500


@mfa_bp.route('/disable', methods=['POST'])
@jwt_required()
def disable_mfa():
    """
    تعطيل المصادقة الثنائية
    Disable MFA for current user.
    
    Request Body:
        token: 6-digit TOTP code for verification
        
    Returns:
        Success status
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({
                'success': False,
                'message': 'الرمز مطلوب للتحقق'
            }), 400
        
        if MFAService.disable_mfa(user_id, data['token']):
            return jsonify({
                'success': True,
                'message': 'تم تعطيل المصادقة الثنائية',
                'message_en': 'MFA disabled successfully'
            })
        
        return jsonify({
            'success': False,
            'message': 'رمز غير صالح'
        }), 400
        
    except Exception as e:
        logger.error(f"MFA disable error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء تعطيل المصادقة الثنائية'
        }), 500


@mfa_bp.route('/status', methods=['GET'])
@jwt_required()
def mfa_status():
    """
    حالة المصادقة الثنائية
    Get MFA status for current user.
    
    Returns:
        MFA status and device info
    """
    try:
        user_id = get_jwt_identity()
        
        is_enabled = MFAService.is_mfa_enabled(user_id)
        devices = MFAService.get_user_devices(user_id)
        backup_count = MFAService.get_backup_codes_count(user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'mfa_enabled': is_enabled,
                'devices': [d.to_dict() for d in devices],
                'backup_codes_remaining': backup_count,
            }
        })
        
    except Exception as e:
        logger.error(f"MFA status error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء جلب حالة المصادقة الثنائية'
        }), 500


@mfa_bp.route('/regenerate-codes', methods=['POST'])
@jwt_required()
def regenerate_backup_codes():
    """
    إعادة إنشاء رموز النسخ الاحتياطي
    Regenerate backup codes (invalidates old ones).
    
    Request Body:
        token: 6-digit TOTP code for verification
        
    Returns:
        New backup codes (only shown once!)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('token'):
            return jsonify({
                'success': False,
                'message': 'الرمز مطلوب للتحقق'
            }), 400
        
        codes = MFAService.regenerate_backup_codes(user_id, data['token'])
        
        if codes:
            return jsonify({
                'success': True,
                'data': {
                    'backup_codes': codes,
                    'warning': 'احفظ هذه الرموز في مكان آمن. لن تظهر مرة أخرى!',
                    'warning_en': 'Save these codes in a safe place. They will not be shown again!'
                },
                'message': 'تم إنشاء رموز جديدة'
            })
        
        return jsonify({
            'success': False,
            'message': 'رمز غير صالح'
        }), 400
        
    except Exception as e:
        logger.error(f"Regenerate codes error: {e}")
        return jsonify({
            'success': False,
            'message': 'حدث خطأ أثناء إعادة إنشاء الرموز'
        }), 500


__all__ = ['mfa_bp']
