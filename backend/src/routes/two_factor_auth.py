"""
Two-Factor Authentication API Routes

Endpoints for managing 2FA settings.

Author: Store ERP Team
Version: 2.0
Last Updated: 2025-12-13
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.utils.two_factor_auth import TwoFactorAuthManager
from src.utils.logger import log_api_request, log_error_with_context
from src.models import db
from datetime import datetime

two_factor_bp = Blueprint('two_factor', __name__, url_prefix='/api/2fa')


@two_factor_bp.route('/enable', methods=['POST'])
@login_required
def enable_2fa():
    """
    Enable 2FA for current user.
    
    Returns:
        JSON response with QR code and backup codes
    """
    start_time = datetime.now()
    
    try:
        # Check if already enabled
        if current_user.two_factor_enabled:
            return jsonify({
                'success': False,
                'error': '2FA is already enabled'
            }), 400
        
        # Enable 2FA
        manager = TwoFactorAuthManager(db.session)
        secret, qr_code, backup_codes = manager.enable_2fa(
            current_user.id,
            current_user.username
        )
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='POST',
            endpoint='/api/2fa/enable',
            user_id=current_user.id,
            status_code=200,
            duration_ms=duration_ms
        )
        
        return jsonify({
            'success': True,
            'data': {
                'qr_code': qr_code,
                'backup_codes': backup_codes,
                'message': 'Scan the QR code with your authenticator app and save the backup codes in a safe place'
            }
        }), 200
        
    except Exception as e:
        log_error_with_context(e, {
            'endpoint': '/api/2fa/enable',
            'user_id': current_user.id
        })
        return jsonify({
            'success': False,
            'error': 'Failed to enable 2FA'
        }), 500


@two_factor_bp.route('/verify', methods=['POST'])
@login_required
def verify_2fa():
    """
    Verify 2FA code after enabling.
    
    Request Body:
        {
            "code": "123456"
        }
    
    Returns:
        JSON response with verification result
    """
    start_time = datetime.now()
    
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code is required'
            }), 400
        
        # Verify code
        manager = TwoFactorAuthManager(db.session)
        is_valid = manager.verify_user_code(current_user.id, code)
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='POST',
            endpoint='/api/2fa/verify',
            user_id=current_user.id,
            status_code=200 if is_valid else 401,
            duration_ms=duration_ms
        )
        
        if is_valid:
            return jsonify({
                'success': True,
                'message': '2FA code verified successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid 2FA code'
            }), 401
        
    except Exception as e:
        log_error_with_context(e, {
            'endpoint': '/api/2fa/verify',
            'user_id': current_user.id
        })
        return jsonify({
            'success': False,
            'error': 'Failed to verify 2FA code'
        }), 500


@two_factor_bp.route('/disable', methods=['POST'])
@login_required
def disable_2fa():
    """
    Disable 2FA for current user.
    
    Request Body:
        {
            "code": "123456",
            "password": "user_password"
        }
    
    Returns:
        JSON response with result
    """
    start_time = datetime.now()
    
    try:
        data = request.get_json()
        code = data.get('code')
        password = data.get('password')
        
        if not code or not password:
            return jsonify({
                'success': False,
                'error': 'Code and password are required'
            }), 400
        
        # Verify password
        if not current_user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid password'
            }), 401
        
        # Verify 2FA code
        manager = TwoFactorAuthManager(db.session)
        if not manager.verify_user_code(current_user.id, code):
            return jsonify({
                'success': False,
                'error': 'Invalid 2FA code'
            }), 401
        
        # Disable 2FA
        success = manager.disable_2fa(current_user.id, current_user.username)
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='POST',
            endpoint='/api/2fa/disable',
            user_id=current_user.id,
            status_code=200 if success else 500,
            duration_ms=duration_ms
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': '2FA disabled successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to disable 2FA'
            }), 500
        
    except Exception as e:
        log_error_with_context(e, {
            'endpoint': '/api/2fa/disable',
            'user_id': current_user.id
        })
        return jsonify({
            'success': False,
            'error': 'Failed to disable 2FA'
        }), 500


@two_factor_bp.route('/regenerate-backup-codes', methods=['POST'])
@login_required
def regenerate_backup_codes():
    """
    Regenerate backup codes for current user.
    
    Request Body:
        {
            "code": "123456"
        }
    
    Returns:
        JSON response with new backup codes
    """
    start_time = datetime.now()
    
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code is required'
            }), 400
        
        # Verify 2FA code
        manager = TwoFactorAuthManager(db.session)
        if not manager.verify_user_code(current_user.id, code):
            return jsonify({
                'success': False,
                'error': 'Invalid 2FA code'
            }), 401
        
        # Regenerate backup codes
        backup_codes = manager.regenerate_backup_codes(
            current_user.id,
            current_user.username
        )
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='POST',
            endpoint='/api/2fa/regenerate-backup-codes',
            user_id=current_user.id,
            status_code=200 if backup_codes else 500,
            duration_ms=duration_ms
        )
        
        if backup_codes:
            return jsonify({
                'success': True,
                'data': {
                    'backup_codes': backup_codes,
                    'message': 'Save these backup codes in a safe place'
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to regenerate backup codes'
            }), 500
        
    except Exception as e:
        log_error_with_context(e, {
            'endpoint': '/api/2fa/regenerate-backup-codes',
            'user_id': current_user.id
        })
        return jsonify({
            'success': False,
            'error': 'Failed to regenerate backup codes'
        }), 500


@two_factor_bp.route('/status', methods=['GET'])
@login_required
def get_2fa_status():
    """
    Get 2FA status for current user.
    
    Returns:
        JSON response with 2FA status
    """
    start_time = datetime.now()
    
    try:
        # Get backup codes count
        backup_codes_count = 0
        if current_user.two_factor_backup_codes:
            backup_codes_count = len(current_user.two_factor_backup_codes.split(','))
        
        # Log API request
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        log_api_request(
            method='GET',
            endpoint='/api/2fa/status',
            user_id=current_user.id,
            status_code=200,
            duration_ms=duration_ms
        )
        
        return jsonify({
            'success': True,
            'data': {
                'enabled': current_user.two_factor_enabled,
                'backup_codes_remaining': backup_codes_count
            }
        }), 200
        
    except Exception as e:
        log_error_with_context(e, {
            'endpoint': '/api/2fa/status',
            'user_id': current_user.id
        })
        return jsonify({
            'success': False,
            'error': 'Failed to get 2FA status'
        }), 500
