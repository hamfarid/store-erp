# Swagger/OpenAPI Documentation Setup

This guide explains how to add interactive API documentation to Gaara ERP v12.

## Quick Setup with drf-spectacular

### Installation

```bash
pip install drf-spectacular
```

### Configuration

Add to `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Gaara ERP v12 API',
    'DESCRIPTION': 'Enterprise Resource Planning System API',
    'VERSION': '12.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'Auth', 'description': 'Authentication & Authorization'},
        {'name': 'Users', 'description': 'User Management'},
        {'name': 'Organizations', 'description': 'Organization Management'},
        {'name': 'Companies', 'description': 'Company Management'},
        {'name': 'Accounting', 'description': 'Financial Operations'},
        {'name': 'Inventory', 'description': 'Stock Management'},
        {'name': 'Sales', 'description': 'Sales Operations'},
        {'name': 'Purchasing', 'description': 'Procurement'},
        {'name': 'HR', 'description': 'Human Resources'},
        {'name': 'AI', 'description': 'AI/ML Features'},
        {'name': 'Agricultural', 'description': 'Agricultural Modules'},
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
    },
    'SECURITY': [
        {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    ],
}
```

### URL Configuration

Add to `urls.py`:

```python
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    ...
    # OpenAPI Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc (alternative documentation)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

## Accessing Documentation

After setup, access:

| URL | Description |
|-----|-------------|
| `/api/docs/` | Swagger UI (interactive) |
| `/api/redoc/` | ReDoc (readable) |
| `/api/schema/` | Raw OpenAPI schema (JSON/YAML) |

## Documenting ViewSets

### Basic Documentation

```python
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

@extend_schema_view(
    list=extend_schema(description='List all users'),
    create=extend_schema(description='Create a new user'),
    retrieve=extend_schema(description='Get user details'),
    update=extend_schema(description='Update user'),
    destroy=extend_schema(description='Delete user'),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### Custom Actions

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

class UserViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary='Activate user account',
        description='Activates a user account by ID',
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='User ID'
            )
        ],
        responses={
            200: {'description': 'User activated successfully'},
            404: {'description': 'User not found'},
        }
    )
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        ...
```

### Request/Response Examples

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    request=UserCreateSerializer,
    responses={201: UserSerializer},
    examples=[
        OpenApiExample(
            'Valid User',
            value={
                'email': 'user@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'SecurePass123!'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Created User',
            value={
                'id': 1,
                'email': 'user@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True,
            },
            response_only=True,
        ),
    ]
)
def create(self, request):
    ...
```

## Authentication in Swagger UI

### JWT Authentication

Users can authenticate in Swagger UI:

1. Click "Authorize" button
2. Enter: `Bearer <your_jwt_token>`
3. Click "Authorize"

### Getting JWT Token

Use the login endpoint:

```bash
POST /api/security/login/
{
    "email": "user@example.com",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Generating Static Schema

```bash
# JSON format
python manage.py spectacular --file schema.json

# YAML format
python manage.py spectacular --file schema.yml --format yaml
```

## Schema Validation

Validate your schema:

```bash
python manage.py spectacular --validate
```

## API Tags

Organize endpoints with tags:

```python
@extend_schema(tags=['Accounting'])
class AccountViewSet(viewsets.ModelViewSet):
    ...
```

## Excluding Endpoints

Hide internal endpoints:

```python
@extend_schema(exclude=True)
class InternalViewSet(viewsets.ModelViewSet):
    ...
```

## Current API Summary

Based on `API_ENDPOINTS.md`, Gaara ERP has:

- **255 total endpoints**
- **30+ modules** (core, admin, business, agricultural, AI, integration, services)
- **Key API groups**:
  - Auth & Security
  - User Management
  - Organization & Companies
  - Accounting & Finance
  - Inventory & Sales
  - HR & Payroll
  - AI/ML Features
  - Agricultural Modules

See `docs/API_ENDPOINTS.md` for the complete endpoint list.

