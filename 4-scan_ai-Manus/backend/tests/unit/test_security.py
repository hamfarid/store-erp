"""
FILE: backend/tests/unit/test_security.py | PURPOSE: Security utilities tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Unit Tests for Security Utilities

Tests for:
- XSS protection
- Input sanitization
- URL validation
- Filename sanitization

Version: 1.0.0
"""

import pytest
import sys
from pathlib import Path

# Add backend src to path
backend_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(backend_src))

from utils.security import (
    XSSProtection,
    InputValidator,
    sanitize_html,
    sanitize_string,
    sanitize_dict,
    sanitize_filename,
    is_safe_url
)


class TestXSSProtection:
    """Test XSS protection utilities"""
    
    def test_sanitize_html_removes_script_tags(self):
        """Test that script tags are removed"""
        html = '<p>Hello</p><script>alert("XSS")</script>'
        result = sanitize_html(html, allow_tags=True)
        assert '<script>' not in result
        assert 'alert' not in result
        assert '<p>Hello</p>' in result
    
    def test_sanitize_html_removes_onclick(self):
        """Test that onclick attributes are removed"""
        html = '<a href="#" onclick="alert(\'XSS\')">Click</a>'
        result = sanitize_html(html, allow_tags=True)
        assert 'onclick' not in result
        assert 'alert' not in result
    
    def test_sanitize_html_allows_safe_tags(self):
        """Test that safe tags are preserved"""
        html = '<p><strong>Bold</strong> and <em>italic</em></p>'
        result = sanitize_html(html, allow_tags=True)
        assert '<strong>Bold</strong>' in result
        assert '<em>italic</em>' in result
    
    def test_sanitize_html_escapes_when_no_tags_allowed(self):
        """Test that HTML is escaped when tags not allowed"""
        html = '<p>Hello</p>'
        result = sanitize_html(html, allow_tags=False)
        assert '&lt;p&gt;Hello&lt;/p&gt;' in result
    
    def test_sanitize_string_removes_html(self):
        """Test that HTML is removed from strings"""
        text = '<script>alert("XSS")</script>Hello'
        result = sanitize_string(text)
        assert '<script>' not in result
        assert 'Hello' in result
    
    def test_sanitize_string_removes_null_bytes(self):
        """Test that null bytes are removed"""
        text = 'Hello\x00World'
        result = sanitize_string(text)
        assert '\x00' not in result
        assert 'HelloWorld' in result
    
    def test_sanitize_dict_sanitizes_all_strings(self):
        """Test that all strings in dict are sanitized"""
        data = {
            'name': '<script>alert("XSS")</script>John',
            'email': 'john@example.com',
            'bio': '<p>Developer</p>'
        }
        result = sanitize_dict(data, allow_html_fields=['bio'])
        assert '<script>' not in result['name']
        assert 'John' in result['name']
        assert result['email'] == 'john@example.com'
        assert '<p>Developer</p>' in result['bio']
    
    def test_sanitize_dict_handles_nested_objects(self):
        """Test that nested objects are sanitized"""
        data = {
            'user': {
                'name': '<script>XSS</script>John',
                'profile': {
                    'bio': '<p>Developer</p>'
                }
            }
        }
        result = sanitize_dict(data)
        assert '<script>' not in result['user']['name']
        assert 'John' in result['user']['name']


class TestInputValidator:
    """Test input validation utilities"""
    
    def test_is_safe_filename_rejects_path_traversal(self):
        """Test that path traversal is rejected"""
        assert not InputValidator.is_safe_filename('../etc/passwd')
        assert not InputValidator.is_safe_filename('..\\windows\\system32')
        assert not InputValidator.is_safe_filename('file/../../../etc/passwd')
    
    def test_is_safe_filename_rejects_null_bytes(self):
        """Test that null bytes are rejected"""
        assert not InputValidator.is_safe_filename('file\x00.txt')
    
    def test_is_safe_filename_rejects_hidden_files(self):
        """Test that hidden files are rejected"""
        assert not InputValidator.is_safe_filename('.htaccess')
        assert not InputValidator.is_safe_filename('.env')
    
    def test_is_safe_filename_accepts_valid_names(self):
        """Test that valid filenames are accepted"""
        assert InputValidator.is_safe_filename('document.pdf')
        assert InputValidator.is_safe_filename('image_2024.jpg')
        assert InputValidator.is_safe_filename('report-final.xlsx')
    
    def test_sanitize_filename_removes_dangerous_chars(self):
        """Test that dangerous characters are removed"""
        filename = '../../../etc/passwd'
        result = sanitize_filename(filename)
        assert '..' not in result
        assert '/' not in result
        assert result == 'etcpasswd'
    
    def test_sanitize_filename_limits_length(self):
        """Test that filename length is limited"""
        filename = 'a' * 300 + '.txt'
        result = sanitize_filename(filename)
        assert len(result) <= 255
    
    def test_is_safe_url_rejects_javascript(self):
        """Test that javascript: URLs are rejected"""
        assert not is_safe_url('javascript:alert("XSS")')
        assert not is_safe_url('JAVASCRIPT:alert("XSS")')
    
    def test_is_safe_url_rejects_data_urls(self):
        """Test that data: URLs are rejected"""
        assert not is_safe_url('data:text/html,<script>alert("XSS")</script>')
    
    def test_is_safe_url_accepts_http_https(self):
        """Test that HTTP/HTTPS URLs are accepted"""
        assert is_safe_url('http://example.com')
        assert is_safe_url('https://example.com')
        assert is_safe_url('https://example.com/path?query=value')
    
    def test_is_safe_url_rejects_invalid_protocols(self):
        """Test that invalid protocols are rejected"""
        assert not is_safe_url('ftp://example.com')
        assert not is_safe_url('file:///etc/passwd')


@pytest.mark.parametrize("input_html,expected", [
    ('<script>alert("XSS")</script>', ''),
    ('<img src=x onerror=alert("XSS")>', ''),
    ('<p>Safe content</p>', '<p>Safe content</p>'),
    ('<a href="javascript:alert()">Click</a>', ''),
])
def test_sanitize_html_parametrized(input_html, expected):
    """Parametrized test for HTML sanitization"""
    result = sanitize_html(input_html, allow_tags=True)
    if expected:
        assert expected in result
    else:
        assert 'script' not in result.lower()
        assert 'alert' not in result.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

