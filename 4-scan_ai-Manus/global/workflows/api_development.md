# 🔌 API Development Workflow

**Version:** 9.0.0  
**Expert:** Backend Expert + Security Expert  
**Estimated Time:** 4-8 hours (depending on complexity)

---

## 📋 Workflow Overview

```
Initialize → Design → Implement → Secure → Test → Document → Deploy
```

---

## 🎯 Phase 1: Initialize (Team Leader)

### **Actions:**
1. **Activate Memory & MCP**
   ```
   memory.save({"type": "project_start", "content": "API Development"})
   mcp.check_servers()
   ```

2. **Understand Requirements**
   - What data needs to be exposed?
   - Who will consume the API?
   - What operations are needed (CRUD)?
   - Performance requirements?
   - Security requirements?

3. **Save Context**
   ```python
   memory.save({
       "type": "api_requirements",
       "content": {
           "endpoints": [...],
           "consumers": [...],
           "security_level": "high",
           "performance_target": "< 200ms"
       }
   })
   ```

4. **Create Mind Map**
   ```
   API Project
   ├── Endpoints
   │   ├── Users (/api/users)
   │   ├── Products (/api/products)
   │   └── Orders (/api/orders)
   ├── Authentication
   │   └── JWT tokens
   ├── Rate Limiting
   └── Documentation
   ```

5. **Assign Experts**
   - Backend Expert (design & implement)
   - Security Expert (secure)
   - Testing Expert (test)

---

## 🔧 Phase 2: Design (Backend Expert)

### **Transform Mindset:**
```
I am a Backend Expert.
I am a genius at API design.
I think about scalability, performance, and maintainability.
I design APIs that are intuitive and powerful.
```

### **Actions:**

1. **Read Rules**
   ```bash
   cat rules/backend.md
   cat rules/api.md  # if exists
   ```

2. **Study Examples**
   ```bash
   ls examples/backend/api_*.py
   ```

3. **Design Endpoints**
   ```
   Resource-based design:
   
   Users:
   GET    /api/v1/users          # List users
   POST   /api/v1/users          # Create user
   GET    /api/v1/users/:id      # Get user
   PUT    /api/v1/users/:id      # Update user
   DELETE /api/v1/users/:id      # Delete user
   
   Products:
   GET    /api/v1/products       # List products
   POST   /api/v1/products       # Create product
   GET    /api/v1/products/:id   # Get product
   PUT    /api/v1/products/:id   # Update product
   DELETE /api/v1/products/:id   # Delete product
   ```

4. **Design Request/Response**
   ```json
   // POST /api/v1/users
   Request:
   {
     "name": "John Doe",
     "email": "john@example.com",
     "role": "user"
   }
   
   Response (201 Created):
   {
     "id": "uuid-123",
     "name": "John Doe",
     "email": "john@example.com",
     "role": "user",
     "created_at": "2025-11-04T10:30:00Z"
   }
   ```

5. **Design Error Responses**
   ```json
   // 400 Bad Request
   {
     "error": {
       "code": "VALIDATION_ERROR",
       "message": "Invalid email format",
       "field": "email"
     }
   }
   
   // 401 Unauthorized
   {
     "error": {
       "code": "UNAUTHORIZED",
       "message": "Invalid or expired token"
     }
   }
   
   // 500 Internal Server Error
   {
     "error": {
       "code": "INTERNAL_ERROR",
       "message": "An unexpected error occurred",
       "request_id": "req-uuid-456"
     }
   }
   ```

6. **Save Design**
   ```python
   memory.save({
       "type": "api_design",
       "content": {
           "endpoints": endpoints_list,
           "request_format": request_schema,
           "response_format": response_schema,
           "error_handling": error_schema
       }
   })
   ```

---

## 💻 Phase 3: Implement (Backend Expert)

### **Actions:**

1. **Set Up Project Structure**
   ```
   project/
   ├── api/
   │   ├── __init__.py
   │   ├── views.py
   │   ├── serializers.py
   │   ├── urls.py
   │   └── permissions.py
   ├── models/
   │   └── user.py
   ├── tests/
   │   └── test_api.py
   └── requirements.txt
   ```

2. **Implement Models** (if needed)
   ```python
   # models/user.py
   from django.db import models
   
   class User(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4)
       name = models.CharField(max_length=255)
       email = models.EmailField(unique=True)
       role = models.CharField(max_length=50, choices=ROLE_CHOICES)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   ```

3. **Implement Serializers**
   ```python
   # api/serializers.py
   from rest_framework import serializers
   
   class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = User
           fields = ['id', 'name', 'email', 'role', 'created_at']
           read_only_fields = ['id', 'created_at']
       
       def validate_email(self, value):
           if not value or '@' not in value:
               raise serializers.ValidationError("Invalid email")
           return value
   ```

4. **Implement Views**
   ```python
   # api/views.py
   from rest_framework import viewsets, status
   from rest_framework.response import Response
   
   class UserViewSet(viewsets.ModelViewSet):
       queryset = User.objects.all()
       serializer_class = UserSerializer
       
       def create(self, request):
           serializer = self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           user = serializer.save()
           return Response(
               serializer.data,
               status=status.HTTP_201_CREATED
           )
   ```

5. **Implement URLs**
   ```python
   # api/urls.py
   from rest_framework.routers import DefaultRouter
   
   router = DefaultRouter()
   router.register(r'users', UserViewSet, basename='user')
   
   urlpatterns = router.urls
   ```

6. **Test Implementation**
   ```bash
   python manage.py runserver
   curl http://localhost:8000/api/v1/users
   ```

7. **Save Progress**
   ```python
   memory.save({
       "type": "implementation_progress",
       "content": {
           "completed": ["models", "serializers", "views", "urls"],
           "files_created": ["models/user.py", "api/serializers.py", ...],
           "status": "implemented"
       }
   })
   ```

---

## 🔒 Phase 4: Secure (Security Expert)

### **Transform Mindset:**
```
I am a Security Expert.
I am paranoid. Everything is a threat.
I secure every endpoint, validate every input, protect every resource.
```

### **Actions:**

1. **Read Rules**
   ```bash
   cat rules/security.md
   ```

2. **Implement Authentication**
   ```python
   # api/authentication.py
   from rest_framework_simplejwt.authentication import JWTAuthentication
   
   class CustomJWTAuthentication(JWTAuthentication):
       def authenticate(self, request):
           # Custom JWT validation
           return super().authenticate(request)
   ```

3. **Implement Permissions**
   ```python
   # api/permissions.py
   from rest_framework.permissions import BasePermission
   
   class IsOwnerOrAdmin(BasePermission):
       def has_object_permission(self, request, view, obj):
           return request.user.is_staff or obj.user == request.user
   ```

4. **Add Rate Limiting**
   ```python
   # settings.py
   REST_FRAMEWORK = {
       'DEFAULT_THROTTLE_CLASSES': [
           'rest_framework.throttling.AnonRateThrottle',
           'rest_framework.throttling.UserRateThrottle'
       ],
       'DEFAULT_THROTTLE_RATES': {
           'anon': '100/hour',
           'user': '1000/hour'
       }
   }
   ```

5. **Add Input Validation**
   ```python
   # api/validators.py
   def validate_user_input(data):
       # Sanitize inputs
       data['name'] = bleach.clean(data.get('name', ''))
       data['email'] = data.get('email', '').lower().strip()
       
       # Validate
       if not data['email'] or '@' not in data['email']:
           raise ValidationError("Invalid email")
       
       return data
   ```

6. **Add CORS**
   ```python
   # settings.py
   CORS_ALLOWED_ORIGINS = [
       "https://example.com",
       "https://app.example.com",
   ]
   ```

7. **Security Audit**
   ```
   ✅ Authentication implemented
   ✅ Authorization implemented
   ✅ Rate limiting enabled
   ✅ Input validation added
   ✅ CORS configured
   ✅ HTTPS enforced
   ✅ SQL injection prevented (ORM)
   ✅ XSS prevented (serializers)
   ```

8. **Handoff to Testing**
   ```python
   memory.save({
       "type": "handoff",
       "from": "Security Expert",
       "to": "Testing Expert",
       "content": {
           "security_implemented": True,
           "vulnerabilities_fixed": [],
           "ready_for_testing": True
       }
   })
   ```

---

## ✅ Phase 5: Test (Testing Expert)

### **Transform Mindset:**
```
I am a Testing Expert.
I am skeptical. I break everything.
I test every endpoint, every edge case, every error condition.
```

### **Actions:**

1. **Read Rules**
   ```bash
   cat rules/testing.md
   ```

2. **Write Unit Tests**
   ```python
   # tests/test_api.py
   from django.test import TestCase
   from rest_framework.test import APIClient
   
   class UserAPITest(TestCase):
       def setUp(self):
           self.client = APIClient()
       
       def test_create_user(self):
           data = {
               "name": "John Doe",
               "email": "john@example.com",
               "role": "user"
           }
           response = self.client.post('/api/v1/users/', data)
           self.assertEqual(response.status_code, 201)
           self.assertEqual(response.data['name'], "John Doe")
       
       def test_create_user_invalid_email(self):
           data = {"name": "John", "email": "invalid"}
           response = self.client.post('/api/v1/users/', data)
           self.assertEqual(response.status_code, 400)
   ```

3. **Write Integration Tests**
   ```python
   def test_user_workflow(self):
       # Create
       response = self.client.post('/api/v1/users/', user_data)
       user_id = response.data['id']
       
       # Read
       response = self.client.get(f'/api/v1/users/{user_id}/')
       self.assertEqual(response.status_code, 200)
       
       # Update
       response = self.client.put(f'/api/v1/users/{user_id}/', updated_data)
       self.assertEqual(response.status_code, 200)
       
       # Delete
       response = self.client.delete(f'/api/v1/users/{user_id}/')
       self.assertEqual(response.status_code, 204)
   ```

4. **Test Security**
   ```python
   def test_authentication_required(self):
       response = self.client.get('/api/v1/users/')
       self.assertEqual(response.status_code, 401)
   
   def test_rate_limiting(self):
       for i in range(150):
           response = self.client.get('/api/v1/users/')
       self.assertEqual(response.status_code, 429)  # Too Many Requests
   ```

5. **Run Tests**
   ```bash
   pytest tests/ -v --cov=api --cov-report=html
   ```

6. **Generate Report**
   ```
   Test Results:
   ✅ 45 tests passed
   ❌ 0 tests failed
   📊 Coverage: 95%
   ⏱️  Duration: 2.3s
   ```

---

## 📚 Phase 6: Document (Backend Expert)

### **Actions:**

1. **Generate API Documentation**
   ```python
   # Use drf-spectacular
   from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
   
   urlpatterns = [
       path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
       path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
   ]
   ```

2. **Write README**
   ```markdown
   # API Documentation
   
   ## Authentication
   Use JWT tokens in Authorization header:
   ```
   Authorization: Bearer <token>
   ```
   
   ## Endpoints
   
   ### Users
   - `GET /api/v1/users/` - List all users
   - `POST /api/v1/users/` - Create a user
   ...
   ```

3. **Add Examples**
   ```markdown
   ## Examples
   
   ### Create User
   ```bash
   curl -X POST https://api.example.com/api/v1/users/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"name": "John Doe", "email": "john@example.com"}'
   ```
   ```

---

## 🚀 Phase 7: Deploy (Team Leader)

### **Actions:**

1. **Review All Work**
   - Check implementation
   - Verify security
   - Review tests
   - Check documentation

2. **Approve**
   ```python
   memory.save({
       "type": "approval",
       "content": {
           "approved": True,
           "quality_score": 95,
           "ready_for_deployment": True
       }
   })
   ```

3. **Deploy** (see deployment workflow)

---

## 📊 Success Criteria

✅ All endpoints implemented  
✅ All tests passing (95%+ coverage)  
✅ Security audit passed  
✅ Documentation complete  
✅ Performance < 200ms  
✅ Rate limiting working  
✅ Error handling robust  

---

## 🎯 Common Pitfalls

❌ **Skipping authentication** - Always secure your API  
❌ **No input validation** - Validate everything  
❌ **Poor error messages** - Be clear and helpful  
❌ **No rate limiting** - Protect against abuse  
❌ **Missing documentation** - Document everything  

---

*Follow this workflow for consistent, secure, well-tested APIs.*
