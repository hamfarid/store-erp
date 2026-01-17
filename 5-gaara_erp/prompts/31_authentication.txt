=================================================================================
AUTHENTICATION SYSTEMS - JWT, OAuth, Social Auth
=================================================================================

Version: 5.0.0
Type: Security - Authentication

Detailed guidance for implementing authentication systems.

=================================================================================
JWT AUTHENTICATION
=================================================================================

## Complete Implementation (FastAPI)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.post("/auth/register")
async def register(user: User):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )
    # Save user to database
    return {"message": "User created"}

@app.post("/auth/login", response_model=Token)
async def login(user: User):
    # Verify user credentials
    # ...
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(payload: dict = Depends(verify_token)):
    return {"message": f"Hello {payload['sub']}"}
```

## Django JWT

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

# Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

=================================================================================
OAUTH 2.0
=================================================================================

## Google OAuth (FastAPI)

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id='your-client-id',
    client_secret='your-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    # Create or update user
    return {"email": user_info['email']}
```

=================================================================================
SOCIAL AUTHENTICATION
=================================================================================

## Django Social Auth

```python
# Install: pip install social-auth-app-django

INSTALLED_APPS = [
    ...
    'social_django',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-client-id'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-client-secret'

# URLs
urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
]
```

=================================================================================
TWO-FACTOR AUTHENTICATION (2FA)
=================================================================================

```python
import pyotp
import qrcode
from io import BytesIO

def generate_totp_secret():
    return pyotp.random_base32()

def generate_qr_code(user_email, secret):
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email,
        issuer_name="MyApp"
    )
    qr = qrcode.QRCode()
    qr.add_data(totp_uri)
    qr.make()
    img = qr.make_image()
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def verify_totp(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

# Usage
@app.post("/auth/2fa/enable")
async def enable_2fa(user_id: int):
    secret = generate_totp_secret()
    # Save secret to user
    qr_code = generate_qr_code(user.email, secret)
    return {"qr_code": qr_code}

@app.post("/auth/2fa/verify")
async def verify_2fa(user_id: int, code: str):
    # Get user's secret
    if verify_totp(user.totp_secret, code):
        return {"message": "2FA verified"}
    raise HTTPException(status_code=400, detail="Invalid code")
```

=================================================================================
PASSWORD RESET
=================================================================================

```python
from itsdangerous import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(email):
    return serializer.dumps(email, salt='password-reset')

def verify_reset_token(token, max_age=3600):
    try:
        email = serializer.loads(
            token,
            salt='password-reset',
            max_age=max_age
        )
        return email
    except:
        return None

@app.post("/auth/forgot-password")
async def forgot_password(email: str):
    token = generate_reset_token(email)
    reset_link = f"https://myapp.com/reset-password?token={token}"
    # Send email with reset_link
    return {"message": "Reset link sent"}

@app.post("/auth/reset-password")
async def reset_password(token: str, new_password: str):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    # Update password
    return {"message": "Password reset successful"}
```

=================================================================================
END OF AUTHENTICATION PROMPT
=================================================================================


================================================================================
CRITICAL MISSING CONTENT - Deep Search Recovery
================================================================================

```python
"""
File: path/to/file.py
Module: module_name
Created: YYYY-MM-DD
Last Modified: YYYY-MM-DD
Author: author_name
Description: Brief description of file purpose

Dependencies:
- dependency1
- dependency2

Related Files:
- related_file1.py
- related_file2.py
"""
```

```python
#!/usr/bin/env python3
"""Add headers to files missing them."""

from pathlib import Path
from datetime import date

PYTHON_TEMPLATE = '''"""
File: {path}
Module: {module}
Created: {date}
Last Modified: {date}
Author: {author}
Description: TODO: Add description

Dependencies:
- TODO: List dependencies

Related Files:
- TODO: List related files
"""

'''

def add_python_header(file_path, author="Team"):
    """Add header to Python file."""
    with open(file_path) as f:
        content = f.read()
    
    if content.startswith('"""'):
        print(f"⏭️  {file_path} already has header")
        return
    
    module = str(file_path).replace('/', '.').replace('.py', '')
    header = PYTHON_TEMPLATE.format(
        path=file_path,
        module=module,
        date=date.today().isoformat(),
        author=author
    )
    
    with open(file_path, 'w') as f:
        f.write(header + content)
    
    print(f"✅ Added header to {file_path}")

def main():
    """Add headers to all Python files."""
    for py_file in Path('.').rglob('*.py'):
        if '__pycache__' not in str(py_file):
            add_python_header(py_file)

if __name__ == '__main__':
    main()
```

