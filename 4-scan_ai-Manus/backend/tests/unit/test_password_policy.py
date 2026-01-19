"""
FILE: backend/tests/unit/test_password_policy.py | PURPOSE: Password policy tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Unit Tests for Password Policy

Tests for:
- Password validation
- Password strength calculation
- Password hashing
- Password history
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
    PasswordPolicy,
    validate_password,
    hash_password,
    verify_password,
    calculate_password_strength
)


class TestPasswordValidation:
    """Test password validation"""
    
    def test_password_too_short(self):
        """Test that short passwords are rejected"""
        is_valid, errors = validate_password('Short1!')
        assert not is_valid
        assert any('12 characters' in error for error in errors)
    
    def test_password_missing_uppercase(self):
        """Test that passwords without uppercase are rejected"""
        is_valid, errors = validate_password('lowercase123!')
        assert not is_valid
        assert any('uppercase' in error for error in errors)
    
    def test_password_missing_lowercase(self):
        """Test that passwords without lowercase are rejected"""
        is_valid, errors = validate_password('UPPERCASE123!')
        assert not is_valid
        assert any('lowercase' in error for error in errors)
    
    def test_password_missing_number(self):
        """Test that passwords without numbers are rejected"""
        is_valid, errors = validate_password('NoNumbersHere!')
        assert not is_valid
        assert any('number' in error for error in errors)
    
    def test_password_missing_special_char(self):
        """Test that passwords without special characters are rejected"""
        is_valid, errors = validate_password('NoSpecialChar123')
        assert not is_valid
        assert any('special character' in error for error in errors)
    
    def test_password_common_password(self):
        """Test that common passwords are rejected"""
        is_valid, errors = validate_password('Password123!')
        assert not is_valid
        assert any('too common' in error for error in errors)
    
    def test_password_sequential_characters(self):
        """Test that sequential characters are rejected"""
        is_valid, errors = validate_password('Abc123456789!')
        assert not is_valid
        assert any('sequential' in error for error in errors)
    
    def test_password_repeated_characters(self):
        """Test that repeated characters are rejected"""
        is_valid, errors = validate_password('Aaa111bbbCCC!')
        assert not is_valid
        assert any('repeated' in error for error in errors)
    
    def test_valid_strong_password(self):
        """Test that valid strong passwords are accepted"""
        is_valid, errors = validate_password('MyStr0ng!P@ssw0rd')
        assert is_valid
        assert len(errors) == 0
    
    def test_password_too_long(self):
        """Test that very long passwords are rejected"""
        long_password = 'A1!' + 'a' * 200
        is_valid, errors = validate_password(long_password)
        assert not is_valid
        assert any('128 characters' in error for error in errors)


class TestPasswordStrength:
    """Test password strength calculation"""
    
    def test_weak_password_score(self):
        """Test that weak passwords get low scores"""
        score, strength = calculate_password_strength('weak')
        assert score < 40
        assert strength == 'Weak'
    
    def test_fair_password_score(self):
        """Test that fair passwords get medium scores"""
        score, strength = calculate_password_strength('Fair1234')
        assert 40 <= score < 60
        assert strength == 'Fair'
    
    def test_good_password_score(self):
        """Test that good passwords get good scores"""
        score, strength = calculate_password_strength('G00dP@ssw0rd')
        assert 60 <= score < 80
        assert strength == 'Good'
    
    def test_strong_password_score(self):
        """Test that strong passwords get high scores"""
        score, strength = calculate_password_strength('V3ry!Str0ng#P@ssw0rd')
        assert score >= 80
        assert strength == 'Strong'
    
    def test_length_affects_score(self):
        """Test that longer passwords get higher scores"""
        score1, _ = calculate_password_strength('Short1!')
        score2, _ = calculate_password_strength('MuchLongerPassword1!')
        assert score2 > score1


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password_returns_hash(self):
        """Test that password hashing returns a hash"""
        password = 'MySecureP@ssw0rd123'
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith('$2b$')  # bcrypt hash
    
    def test_verify_password_correct(self):
        """Test that correct password verification works"""
        password = 'MySecureP@ssw0rd123'
        hashed = hash_password(password)
        assert verify_password(password, hashed)
    
    def test_verify_password_incorrect(self):
        """Test that incorrect password verification fails"""
        password = 'MySecureP@ssw0rd123'
        hashed = hash_password(password)
        assert not verify_password('WrongPassword123!', hashed)
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)"""
        password = 'MySecureP@ssw0rd123'
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2  # Different due to random salt


class TestPasswordHistory:
    """Test password history checking"""
    
    def test_check_password_history_new_password(self):
        """Test that new passwords are accepted"""
        new_password = 'NewP@ssw0rd123'
        history = [
            hash_password('OldP@ssw0rd1'),
            hash_password('OldP@ssw0rd2'),
            hash_password('OldP@ssw0rd3'),
        ]
        assert PasswordPolicy.check_password_history(new_password, history)
    
    def test_check_password_history_reused_password(self):
        """Test that reused passwords are rejected"""
        password = 'ReusedP@ssw0rd123'
        history = [
            hash_password('OldP@ssw0rd1'),
            hash_password(password),  # This password was used before
            hash_password('OldP@ssw0rd3'),
        ]
        assert not PasswordPolicy.check_password_history(password, history)
    
    def test_check_password_history_respects_limit(self):
        """Test that only last N passwords are checked"""
        password = 'OldP@ssw0rd1'
        history = [
            hash_password(password),  # 6th password (should not be checked)
            hash_password('OldP@ssw0rd2'),
            hash_password('OldP@ssw0rd3'),
            hash_password('OldP@ssw0rd4'),
            hash_password('OldP@ssw0rd5'),
            hash_password('OldP@ssw0rd6'),
        ]
        # Should be accepted because it's beyond the 5-password limit
        assert PasswordPolicy.check_password_history(password, history)


class TestPasswordExpiry:
    """Test password expiry"""
    
    def test_password_not_expired(self):
        """Test that recent passwords are not expired"""
        last_changed = datetime.now() - timedelta(days=30)
        assert not PasswordPolicy.is_password_expired(last_changed)
    
    def test_password_expired(self):
        """Test that old passwords are expired"""
        last_changed = datetime.now() - timedelta(days=91)
        assert PasswordPolicy.is_password_expired(last_changed)
    
    def test_password_expiry_boundary(self):
        """Test password expiry at boundary (90 days)"""
        last_changed = datetime.now() - timedelta(days=90, hours=1)
        assert PasswordPolicy.is_password_expired(last_changed)


class TestAccountLockout:
    """Test account lockout"""
    
    def test_no_lockout_below_threshold(self):
        """Test that accounts are not locked below threshold"""
        assert not PasswordPolicy.should_lockout_account(4)
    
    def test_lockout_at_threshold(self):
        """Test that accounts are locked at threshold"""
        last_attempt = datetime.now()
        assert PasswordPolicy.should_lockout_account(5, last_attempt)
    
    def test_lockout_expires(self):
        """Test that lockout expires after duration"""
        last_attempt = datetime.now() - timedelta(minutes=31)
        assert not PasswordPolicy.should_lockout_account(5, last_attempt)
    
    def test_lockout_active_within_duration(self):
        """Test that lockout is active within duration"""
        last_attempt = datetime.now() - timedelta(minutes=15)
        assert PasswordPolicy.should_lockout_account(5, last_attempt)


@pytest.mark.parametrize("password,expected_valid", [
    ('MyStr0ng!P@ssw0rd', True),
    ('weak', False),
    ('NoNumbers!', False),
    ('nonumbers123', False),
    ('NOLOWERCASE123!', False),
    ('NoSpecialChar123', False),
    ('password123!', False),  # Common password
])
def test_password_validation_parametrized(password, expected_valid):
    """Parametrized test for password validation"""
    is_valid, _ = validate_password(password)
    assert is_valid == expected_valid


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

