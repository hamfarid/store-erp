#!/bin/bash
# =============================================================================
# Gaara ERP - Secret Key Generator
# =============================================================================
# Generates secure secret keys for Django
# =============================================================================

echo "=========================================="
echo "Gaara ERP - Secret Key Generator"
echo "=========================================="
echo ""

# Check if openssl is available
if command -v openssl &> /dev/null; then
    echo "Generating secret keys using OpenSSL..."
    echo ""
    echo "SECRET_KEY:"
    openssl rand -hex 32
    echo ""
    echo "ENCRYPTION_KEY:"
    openssl rand -hex 32
    echo ""
    echo "JWT_SECRET_KEY:"
    openssl rand -hex 32
elif command -v python3 &> /dev/null; then
    echo "Generating secret keys using Python..."
    echo ""
    python3 << EOF
import secrets
print("SECRET_KEY:")
print(secrets.token_hex(32))
print("")
print("ENCRYPTION_KEY:")
print(secrets.token_hex(32))
print("")
print("JWT_SECRET_KEY:")
print(secrets.token_hex(32))
EOF
else
    echo "Error: Neither openssl nor python3 found"
    exit 1
fi

echo ""
echo "=========================================="
echo "Copy these keys to your .env file"
echo "=========================================="
