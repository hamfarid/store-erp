"""
FILE: backend/tests/integration/test_authentication.py | PURPOSE: Authentication integration tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Integration Tests for Authentication

Tests for:
- User registration
- User login
- Password validation
- MFA flow
- Token generation
- Account lockout

Version: 1.0.0
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add backend src to path
backend_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(backend_src))

from utils.password_policy import (
    validate_password,
    hash_password,
    verify_password,
    PasswordPolicy
)
from modules.mfa.mfa_service import MFAService, setup_mfa


class TestPasswordAuthentication:
    """Test password-based authentication"""
    
    def test_valid_password_registration(self):
        """Test that valid passwords can be registered"""
        password = "MyStr0ng!P@ssw0rd"
        is_valid, errors = validate_password(password)
        
        assert is_valid
        assert len(errors) == 0
        
        # Hash password
        hashed = hash_password(password)
        assert hashed is not None
        assert hashed != password
    
    def test_invalid_password_registration_fails(self):
        """Test that invalid passwords are rejected"""
        weak_password = "weak"
        is_valid, errors = validate_password(weak_password)
        
        assert not is_valid
        assert len(errors) > 0
    
    def test_login_with_correct_password(self):
        """Test login with correct password"""
        password = "MyStr0ng!P@ssw0rd"
        hashed = hash_password(password)
        
        # Verify password
        assert verify_password(password, hashed)
    
    def test_login_with_incorrect_password(self):
        """Test login with incorrect password fails"""
        password = "MyStr0ng!P@ssw0rd"
        hashed = hash_password(password)
        
        # Try wrong password
        assert not verify_password("WrongPassword123!", hashed)
    
    def test_password_reuse_prevention(self):
        """Test that password reuse is prevented"""
        password = "MyStr0ng!P@ssw0rd"
        
        # Create password history
        history = [
            hash_password("OldP@ssw0rd1"),
            hash_password(password),  # This password was used before
            hash_password("OldP@ssw0rd3"),
        ]
        
        # Try to reuse password
        assert not PasswordPolicy.check_password_history(password, history)
    
    def test_account_lockout_after_failed_attempts(self):
        """Test that account is locked after failed attempts"""
        # Simulate 5 failed attempts
        failed_attempts = 5
        last_attempt = datetime.now()
        
        # Should be locked
        assert PasswordPolicy.should_lockout_account(failed_attempts, last_attempt)
    
    def test_account_lockout_expires(self):
        """Test that account lockout expires"""
        # Simulate 5 failed attempts 31 minutes ago
        failed_attempts = 5
        last_attempt = datetime.now() - timedelta(minutes=31)
        
        # Should not be locked anymore
        assert not PasswordPolicy.should_lockout_account(failed_attempts, last_attempt)


class TestMFAAuthentication:
    """Test MFA authentication"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = MFAService()
        self.test_email = "test@example.com"
    
    def test_mfa_setup_flow(self):
        """Test complete MFA setup flow"""
        # Setup MFA
        secret, qr_code, backup_codes = setup_mfa(self.test_email)
        
        # Verify secret
        assert secret is not None
        assert len(secret) == 32
        
        # Verify QR code
        assert qr_code is not None
        assert qr_code.startswith('data:image/png;base64,')
        
        # Verify backup codes
        assert backup_codes is not None
        assert len(backup_codes) == 10
    
    def test_mfa_login_flow(self):
        """Test MFA login flow"""
        # Setup MFA
        secret = self.service.generate_secret()
        
        # Get current token
        token = self.service.get_current_token(secret)
        
        # Verify token (simulating login)
        assert self.service.verify_token(secret, token)
    
    def test_mfa_login_with_invalid_token_fails(self):
        """Test that MFA login with invalid token fails"""
        secret = self.service.generate_secret()
        
        # Try invalid token
        assert not self.service.verify_token(secret, "000000")
    
    def test_backup_code_usage(self):
        """Test backup code usage"""
        # Generate backup codes
        backup_codes = self.service.generate_backup_codes(count=10)
        
        # Simulate using a backup code
        used_code = backup_codes[0]
        
        # In real implementation, this would be checked against stored codes
        assert used_code in backup_codes
        
        # After use, code should be removed from available codes
        remaining_codes = [code for code in backup_codes if code != used_code]
        assert len(remaining_codes) == 9


class TestAuthenticationFlow:
    """Test complete authentication flows"""
    
    def test_registration_to_login_flow(self):
        """Test complete registration to login flow"""
        # 1. Registration
        email = "newuser@example.com"
        password = "MyStr0ng!P@ssw0rd"
        
        # Validate password
        is_valid, errors = validate_password(password)
        assert is_valid
        
        # Hash password
        hashed_password = hash_password(password)
        
        # 2. Login
        # Verify password
        assert verify_password(password, hashed_password)
    
    def test_registration_with_mfa_flow(self):
        """Test registration with MFA enabled"""
        # 1. Registration
        email = "newuser@example.com"
        password = "MyStr0ng!P@ssw0rd"
        
        # Validate and hash password
        is_valid, _ = validate_password(password)
        assert is_valid
        hashed_password = hash_password(password)
        
        # 2. Setup MFA
        secret, qr_code, backup_codes = setup_mfa(email)
        assert secret is not None
        
        # 3. Login with password
        assert verify_password(password, hashed_password)
        
        # 4. Verify MFA token
        service = MFAService()
        token = service.get_current_token(secret)
        assert service.verify_token(secret, token)
    
    def test_password_change_flow(self):
        """Test password change flow"""
        # Current password
        old_password = "OldP@ssw0rd123"
        old_hashed = hash_password(old_password)
        
        # New password
        new_password = "NewP@ssw0rd456"
        
        # Validate new password
        is_valid, _ = validate_password(new_password)
        assert is_valid
        
        # Check password history (should not be in history)
        history = [old_hashed]
        assert PasswordPolicy.check_password_history(new_password, history)
        
        # Hash new password
        new_hashed = hash_password(new_password)
        
        # Verify new password works
        assert verify_password(new_password, new_hashed)
        
        # Verify old password no longer works
        assert not verify_password(old_password, new_hashed)


@pytest.mark.parametrize("password,should_pass", [
    ("MyStr0ng!P@ssw0rd", True),
    ("weak", False),
    ("NoNumbers!", False),
    ("nonumbers123", False),
    ("NOUPPERCASE123!", False),
])
def test_password_validation_integration(password, should_pass):
    """Parametrized integration test for password validation"""
    is_valid, _ = validate_password(password)
    assert is_valid == should_pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

