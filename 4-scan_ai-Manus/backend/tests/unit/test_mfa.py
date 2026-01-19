"""
FILE: backend/tests/unit/test_mfa.py | PURPOSE: MFA service tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Unit Tests for MFA Service

Tests for:
- TOTP generation and validation
- QR code generation
- Backup codes generation
- MFA policy enforcement

Version: 1.0.0
"""

import pytest
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta

# Add backend src to path
backend_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(backend_src))

from modules.mfa.mfa_service import (
    MFAService,
    MFAPolicy,
    setup_mfa,
    verify_mfa_token
)


class TestMFAService:
    """Test MFA service"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = MFAService()
        self.test_email = 'test@example.com'
    
    def test_generate_secret(self):
        """Test that secret generation works"""
        secret = self.service.generate_secret()
        assert secret is not None
        assert len(secret) == 32  # Base32 encoded
        assert secret.isalnum()
        assert secret.isupper()
    
    def test_generate_qr_code(self):
        """Test that QR code generation works"""
        secret = self.service.generate_secret()
        qr_code = self.service.generate_qr_code(secret, self.test_email)
        
        assert qr_code is not None
        assert qr_code.startswith('data:image/png;base64,')
        assert len(qr_code) > 100  # QR code should be substantial
    
    def test_verify_token_valid(self):
        """Test that valid tokens are accepted"""
        secret = self.service.generate_secret()
        token = self.service.get_current_token(secret)
        
        assert self.service.verify_token(secret, token)
    
    def test_verify_token_invalid(self):
        """Test that invalid tokens are rejected"""
        secret = self.service.generate_secret()
        invalid_token = '000000'
        
        assert not self.service.verify_token(secret, invalid_token)
    
    def test_verify_token_empty(self):
        """Test that empty tokens are rejected"""
        secret = self.service.generate_secret()
        
        assert not self.service.verify_token(secret, '')
        assert not self.service.verify_token('', '123456')
    
    def test_verify_token_with_window(self):
        """Test that tokens within time window are accepted"""
        secret = self.service.generate_secret()
        token = self.service.get_current_token(secret)
        
        # Should work with window=1 (±30 seconds)
        assert self.service.verify_token(secret, token, window=1)
    
    def test_generate_backup_codes(self):
        """Test that backup codes are generated correctly"""
        codes = self.service.generate_backup_codes(count=10)

        assert len(codes) == 10
        assert all(len(code) == 9 for code in codes)  # XXXX-XXXX format
        assert all('-' in code for code in codes)
        # Check that letters are uppercase (ignoring hyphen)
        assert all(code.replace('-', '').isupper() for code in codes)

        # Check format (XXXX-XXXX)
        pattern = r'^[A-F0-9]{4}-[A-F0-9]{4}$'
        assert all(re.match(pattern, code) for code in codes)
    
    def test_backup_codes_unique(self):
        """Test that backup codes are unique"""
        codes = self.service.generate_backup_codes(count=10)
        assert len(codes) == len(set(codes))  # All unique
    
    def test_get_time_remaining(self):
        """Test that time remaining calculation works"""
        remaining = self.service.get_time_remaining()
        assert 0 < remaining <= 30


class TestMFAPolicy:
    """Test MFA policy enforcement"""
    
    def test_mfa_required_for_admin(self):
        """Test that MFA is always required for admins"""
        assert MFAPolicy.is_mfa_required(
            user_role='ADMIN',
            action='any_action'
        )
    
    def test_mfa_not_required_for_regular_user(self):
        """Test that MFA is not required for regular users by default"""
        assert not MFAPolicy.is_mfa_required(
            user_role='USER',
            action='view_dashboard'
        )
    
    def test_mfa_required_for_sensitive_actions(self):
        """Test that MFA is required for sensitive actions"""
        sensitive_actions = [
            'delete_user',
            'change_permissions',
            'export_data',
            'modify_settings',
            'access_admin_panel'
        ]
        
        for action in sensitive_actions:
            assert MFAPolicy.is_mfa_required(
                user_role='USER',
                action=action
            )
    
    def test_mfa_required_after_timeout(self):
        """Test that MFA is required after timeout"""
        last_mfa_time = datetime.now() - timedelta(hours=2)
        
        assert MFAPolicy.is_mfa_required(
            user_role='USER',
            action='view_dashboard',
            last_mfa_time=last_mfa_time
        )
    
    def test_mfa_not_required_within_timeout(self):
        """Test that MFA is not required within timeout"""
        last_mfa_time = datetime.now() - timedelta(minutes=30)
        
        assert not MFAPolicy.is_mfa_required(
            user_role='USER',
            action='view_dashboard',
            last_mfa_time=last_mfa_time
        )


class TestMFAConvenienceFunctions:
    """Test convenience functions"""
    
    def test_setup_mfa(self):
        """Test MFA setup convenience function"""
        secret, qr_code, backup_codes = setup_mfa('test@example.com')
        
        assert secret is not None
        assert len(secret) == 32
        
        assert qr_code is not None
        assert qr_code.startswith('data:image/png;base64,')
        
        assert backup_codes is not None
        assert len(backup_codes) == 10
    
    def test_verify_mfa_token_valid(self):
        """Test MFA token verification convenience function"""
        service = MFAService()
        secret = service.generate_secret()
        token = service.get_current_token(secret)
        
        assert verify_mfa_token(secret, token)
    
    def test_verify_mfa_token_invalid(self):
        """Test MFA token verification with invalid token"""
        service = MFAService()
        secret = service.generate_secret()
        
        assert not verify_mfa_token(secret, '000000')


@pytest.mark.parametrize("role,action,expected", [
    ('ADMIN', 'any_action', True),
    ('MANAGER', 'view_dashboard', False),
    ('USER', 'delete_user', True),
    ('USER', 'export_data', True),
    ('GUEST', 'view_dashboard', False),
])
def test_mfa_policy_parametrized(role, action, expected):
    """Parametrized test for MFA policy"""
    result = MFAPolicy.is_mfa_required(
        user_role=role,
        action=action
    )
    assert result == expected


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

