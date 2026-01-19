"""
Tenant API Routes
مسارات API للمستأجر

RESTful API endpoints for tenant management.

Author: Global v35.0 Singularity
Version: 1.0.0
Created: 2026-01-17
"""

import logging
from typing import Dict, Any

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

logger = logging.getLogger(__name__)


class TenantListCreateView(APIView):
    """
    API view for listing and creating tenants.
    عرض API لقائمة وإنشاء المستأجرين.

    GET: List all tenants (admin only)
    POST: Create a new tenant

    Attributes:
        permission_classes: Requires authentication

    Example:
        GET /api/tenants/
        POST /api/tenants/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        List all tenants.

        For admins: Returns all tenants
        For users: Returns only their tenants

        Args:
            request: HTTP request

        Returns:
            Response: List of tenants

        Example Response:
            {
                "success": true,
                "data": [
                    {
                        "id": "uuid",
                        "name": "Acme Corp",
                        "slug": "acme-corp",
                        "status": "active"
                    }
                ],
                "count": 1
            }
        """
        from backend.src.services.tenant_service import tenant_service

        try:
            if request.user.is_superuser:
                # Admin gets all tenants
                from backend.src.models.tenant import Tenant
                tenants = Tenant.objects.select_related('plan').all()
            else:
                # User gets their tenants
                tenants = tenant_service.get_user_tenants(str(request.user.id))

            data = []
            for tenant in tenants:
                data.append({
                    'id': str(tenant.id),
                    'name': tenant.name,
                    'name_ar': tenant.name_ar,
                    'slug': tenant.slug,
                    'logo': tenant.logo,
                    'status': tenant.status,
                    'is_active': tenant.is_active,
                    'plan': {
                        'code': tenant.plan.code,
                        'name': tenant.plan.name
                    } if tenant.plan else None,
                    'created_at': tenant.created_at.isoformat()
                })

            return Response({
                'success': True,
                'data': data,
                'count': len(data)
            })

        except Exception as e:
            logger.error(f"Error listing tenants: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'LIST_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request) -> Response:
        """
        Create a new tenant.

        Required fields:
        - name: Organization name
        - slug: URL-safe unique identifier

        Optional fields:
        - name_ar: Arabic name
        - plan_code: Subscription plan
        - custom_domain: Custom domain

        Args:
            request: HTTP request with JSON body

        Returns:
            Response: Created tenant data

        Example Request:
            {
                "name": "Acme Corporation",
                "slug": "acme-corp",
                "name_ar": "شركة أكمي",
                "plan_code": "pro"
            }
        """
        from backend.src.services.tenant_service import (
            tenant_service, TenantExistsError, TenantServiceError
        )

        try:
            data = request.data

            # Validate required fields
            if not data.get('name'):
                return Response({
                    'success': False,
                    'error': 'VALIDATION_ERROR',
                    'message': 'Name is required',
                    'message_ar': 'الاسم مطلوب'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not data.get('slug'):
                return Response({
                    'success': False,
                    'error': 'VALIDATION_ERROR',
                    'message': 'Slug is required',
                    'message_ar': 'المعرف الفريد مطلوب'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create tenant
            tenant = tenant_service.create_tenant(
                name=data['name'],
                slug=data['slug'],
                owner=request.user,
                name_ar=data.get('name_ar', ''),
                plan_code=data.get('plan_code', 'basic'),
                custom_domain=data.get('custom_domain'),
                settings_override=data.get('settings'),
                trial_days=data.get('trial_days', 14)
            )

            return Response({
                'success': True,
                'message': 'Tenant created successfully',
                'message_ar': 'تم إنشاء المستأجر بنجاح',
                'data': {
                    'id': str(tenant.id),
                    'name': tenant.name,
                    'slug': tenant.slug,
                    'schema_name': tenant.schema_name,
                    'status': tenant.status,
                    'trial_ends_at': tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None
                }
            }, status=status.HTTP_201_CREATED)

        except TenantExistsError as e:
            return Response({
                'success': False,
                'error': e.code,
                'message': str(e),
                'message_ar': e.message_ar
            }, status=status.HTTP_409_CONFLICT)

        except TenantServiceError as e:
            return Response({
                'success': False,
                'error': e.code,
                'message': str(e),
                'message_ar': e.message_ar
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error creating tenant: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'CREATE_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TenantDetailView(APIView):
    """
    API view for tenant details, update, and delete.
    عرض API لتفاصيل المستأجر والتحديث والحذف.

    GET: Get tenant details
    PUT: Update tenant
    DELETE: Deactivate tenant

    Example:
        GET /api/tenants/{id}/
        PUT /api/tenants/{id}/
        DELETE /api/tenants/{id}/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id: str) -> Response:
        """
        Get tenant details.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant

        Returns:
            Response: Tenant details
        """
        from backend.src.models.tenant import Tenant, TenantUser

        try:
            tenant = Tenant.objects.select_related('plan', 'owner').get(id=tenant_id)

            # Check permission
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN',
                        'message': 'You do not have access to this tenant',
                        'message_ar': 'ليس لديك حق الوصول إلى هذا المستأجر'
                    }, status=status.HTTP_403_FORBIDDEN)

            # Get settings
            settings_data = {}
            try:
                settings = tenant.extended_settings
                settings_data = {
                    'timezone': settings.timezone,
                    'language': settings.language,
                    'currency': settings.currency,
                    'modules_enabled': settings.modules_enabled
                }
            except Exception:
                pass

            return Response({
                'success': True,
                'data': {
                    'id': str(tenant.id),
                    'name': tenant.name,
                    'name_ar': tenant.name_ar,
                    'slug': tenant.slug,
                    'schema_name': tenant.schema_name,
                    'custom_domain': tenant.custom_domain,
                    'logo': tenant.logo,
                    'status': tenant.status,
                    'is_active': tenant.is_active,
                    'owner': {
                        'id': str(tenant.owner.id),
                        'email': tenant.owner.email,
                        'name': getattr(tenant.owner, 'get_full_name', lambda: tenant.owner.email)()
                    },
                    'plan': {
                        'id': str(tenant.plan.id),
                        'code': tenant.plan.code,
                        'name': tenant.plan.name,
                        'max_users': tenant.plan.max_users,
                        'max_storage_gb': tenant.plan.max_storage_gb
                    } if tenant.plan else None,
                    'settings': settings_data,
                    'trial_ends_at': tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None,
                    'subscription_ends_at': tenant.subscription_ends_at.isoformat() if tenant.subscription_ends_at else None,
                    'created_at': tenant.created_at.isoformat(),
                    'updated_at': tenant.updated_at.isoformat()
                }
            })

        except Tenant.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND',
                'message': 'Tenant not found',
                'message_ar': 'المستأجر غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error getting tenant: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'GET_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, tenant_id: str) -> Response:
        """
        Update tenant information.

        Updateable fields:
        - name, name_ar
        - logo
        - custom_domain
        - settings

        Args:
            request: HTTP request with JSON body
            tenant_id: UUID of tenant

        Returns:
            Response: Updated tenant data
        """
        from backend.src.services.tenant_service import (
            tenant_service, TenantExistsError, TenantServiceError
        )
        from backend.src.models.tenant import Tenant, TenantUser

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission (must be owner or admin)
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    role__in=['owner', 'admin'],
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN',
                        'message': 'You do not have permission to update this tenant',
                        'message_ar': 'ليس لديك صلاحية لتحديث هذا المستأجر'
                    }, status=status.HTTP_403_FORBIDDEN)

            # Update tenant
            data = request.data
            updated = tenant_service.update_tenant(
                tenant_id=tenant_id,
                **data
            )

            return Response({
                'success': True,
                'message': 'Tenant updated successfully',
                'message_ar': 'تم تحديث المستأجر بنجاح',
                'data': {
                    'id': str(updated.id),
                    'name': updated.name,
                    'slug': updated.slug,
                    'updated_at': updated.updated_at.isoformat()
                }
            })

        except Tenant.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND',
                'message': 'Tenant not found',
                'message_ar': 'المستأجر غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)

        except TenantExistsError as e:
            return Response({
                'success': False,
                'error': e.code,
                'message': str(e),
                'message_ar': e.message_ar
            }, status=status.HTTP_409_CONFLICT)

        except Exception as e:
            logger.error(f"Error updating tenant: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'UPDATE_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, tenant_id: str) -> Response:
        """
        Deactivate a tenant (soft delete).

        This doesn't delete data, just marks tenant as inactive.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant

        Returns:
            Response: Deactivation confirmation
        """
        from backend.src.services.tenant_service import tenant_service
        from backend.src.models.tenant import Tenant, TenantUser

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission (must be owner or superuser)
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    role='owner',
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN',
                        'message': 'Only owner can deactivate tenant',
                        'message_ar': 'المالك فقط يمكنه إلغاء تنشيط المستأجر'
                    }, status=status.HTTP_403_FORBIDDEN)

            reason = request.data.get('reason', 'User requested')
            tenant_service.deactivate_tenant(tenant_id, reason)

            return Response({
                'success': True,
                'message': 'Tenant deactivated successfully',
                'message_ar': 'تم إلغاء تنشيط المستأجر بنجاح'
            })

        except Tenant.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND',
                'message': 'Tenant not found',
                'message_ar': 'المستأجر غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error deactivating tenant: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'DELETE_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TenantSettingsView(APIView):
    """
    API view for tenant settings.
    عرض API لإعدادات المستأجر.

    GET: Get tenant settings
    PUT: Update tenant settings
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id: str) -> Response:
        """
        Get tenant settings.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant

        Returns:
            Response: Tenant settings
        """
        from backend.src.models.tenant import Tenant, TenantSettings, TenantUser

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            try:
                settings = tenant.extended_settings
                return Response({
                    'success': True,
                    'data': {
                        'timezone': settings.timezone,
                        'language': settings.language,
                        'secondary_language': settings.secondary_language,
                        'date_format': settings.date_format,
                        'time_format': settings.time_format,
                        'currency': settings.currency,
                        'currency_symbol': settings.currency_symbol,
                        'fiscal_year_start_month': settings.fiscal_year_start_month,
                        'modules_enabled': settings.modules_enabled,
                        'theme_settings': settings.theme_settings,
                        'notification_settings': settings.notification_settings,
                        'security_settings': settings.security_settings
                    }
                })
            except TenantSettings.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'SETTINGS_NOT_FOUND',
                    'message': 'Settings not configured for this tenant',
                    'message_ar': 'الإعدادات غير مهيأة لهذا المستأجر'
                }, status=status.HTTP_404_NOT_FOUND)

        except Tenant.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, tenant_id: str) -> Response:
        """
        Update tenant settings.

        Args:
            request: HTTP request with settings data
            tenant_id: UUID of tenant

        Returns:
            Response: Updated settings
        """
        from backend.src.models.tenant import Tenant, TenantSettings, TenantUser

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission (admin only)
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    role__in=['owner', 'admin'],
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            settings, created = TenantSettings.objects.get_or_create(
                tenant=tenant
            )

            data = request.data
            allowed_fields = [
                'timezone', 'language', 'secondary_language',
                'date_format', 'time_format', 'currency', 'currency_symbol',
                'fiscal_year_start_month', 'modules_enabled',
                'theme_settings', 'notification_settings', 'security_settings'
            ]

            for field in allowed_fields:
                if field in data:
                    setattr(settings, field, data[field])

            settings.save()

            return Response({
                'success': True,
                'message': 'Settings updated successfully',
                'message_ar': 'تم تحديث الإعدادات بنجاح'
            })

        except Exception as e:
            logger.error(f"Error updating settings: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'UPDATE_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TenantUsersView(APIView):
    """
    API view for tenant users management.
    عرض API لإدارة مستخدمي المستأجر.

    GET: List tenant users
    POST: Add user to tenant
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, tenant_id: str) -> Response:
        """
        List all users in a tenant.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant

        Returns:
            Response: List of tenant users
        """
        from backend.src.services.tenant_service import tenant_service
        from backend.src.models.tenant import Tenant, TenantUser

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            users = tenant_service.get_tenant_users(tenant_id)

            data = []
            for tu in users:
                data.append({
                    'id': str(tu.id),
                    'user': {
                        'id': str(tu.user.id),
                        'email': tu.user.email,
                        'name': getattr(tu.user, 'get_full_name', lambda: tu.user.email)()
                    },
                    'role': tu.role,
                    'is_primary': tu.is_primary,
                    'is_active': tu.is_active,
                    'joined_at': tu.joined_at.isoformat(),
                    'last_accessed_at': tu.last_accessed_at.isoformat() if tu.last_accessed_at else None
                })

            return Response({
                'success': True,
                'data': data,
                'count': len(data)
            })

        except Tenant.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, tenant_id: str) -> Response:
        """
        Add a user to tenant.

        Required:
        - user_id: UUID of user to add

        Optional:
        - role: Role to assign (default: member)

        Args:
            request: HTTP request
            tenant_id: UUID of tenant

        Returns:
            Response: Created membership
        """
        from backend.src.services.tenant_service import (
            tenant_service, TenantQuotaExceededError
        )
        from backend.src.models.tenant import Tenant, TenantUser
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Check permission (admin only)
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant=tenant,
                    user=request.user,
                    role__in=['owner', 'admin'],
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            user_id = data.get('user_id')
            if not user_id:
                return Response({
                    'success': False,
                    'error': 'VALIDATION_ERROR',
                    'message': 'user_id is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'USER_NOT_FOUND',
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            tenant_user = tenant_service.add_user_to_tenant(
                tenant_id=tenant_id,
                user=user,
                role=data.get('role', 'member'),
                permissions=data.get('permissions')
            )

            return Response({
                'success': True,
                'message': 'User added to tenant',
                'message_ar': 'تم إضافة المستخدم للمستأجر',
                'data': {
                    'id': str(tenant_user.id),
                    'role': tenant_user.role
                }
            }, status=status.HTTP_201_CREATED)

        except TenantQuotaExceededError as e:
            return Response({
                'success': False,
                'error': e.code,
                'message': str(e),
                'message_ar': e.message_ar
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            logger.error(f"Error adding user: {e}", exc_info=True)
            return Response({
                'success': False,
                'error': 'ADD_ERROR',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TenantUserDetailView(APIView):
    """
    API view for managing individual tenant user.
    عرض API لإدارة مستخدم مستأجر فردي.

    PUT: Update user role/permissions
    DELETE: Remove user from tenant
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, tenant_id: str, user_id: str) -> Response:
        """
        Update tenant user role or permissions.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant
            user_id: UUID of user

        Returns:
            Response: Updated membership
        """
        from backend.src.models.tenant import TenantUser

        try:
            tenant_user = TenantUser.objects.get(
                tenant_id=tenant_id,
                user_id=user_id
            )

            # Check permission
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant_id=tenant_id,
                    user=request.user,
                    role__in=['owner', 'admin'],
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            # Cannot change owner's role
            if tenant_user.role == 'owner':
                return Response({
                    'success': False,
                    'error': 'CANNOT_MODIFY_OWNER',
                    'message': 'Cannot modify owner role',
                    'message_ar': 'لا يمكن تعديل دور المالك'
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            if 'role' in data:
                tenant_user.role = data['role']
            if 'permissions' in data:
                tenant_user.permissions = data['permissions']
            if 'is_active' in data:
                tenant_user.is_active = data['is_active']

            tenant_user.save()

            return Response({
                'success': True,
                'message': 'User updated',
                'message_ar': 'تم تحديث المستخدم'
            })

        except TenantUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'NOT_FOUND'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, tenant_id: str, user_id: str) -> Response:
        """
        Remove user from tenant.

        Args:
            request: HTTP request
            tenant_id: UUID of tenant
            user_id: UUID of user

        Returns:
            Response: Confirmation
        """
        from backend.src.services.tenant_service import tenant_service
        from backend.src.models.tenant import TenantUser

        try:
            # Check permission
            if not request.user.is_superuser:
                membership = TenantUser.objects.filter(
                    tenant_id=tenant_id,
                    user=request.user,
                    role__in=['owner', 'admin'],
                    is_active=True
                ).first()
                if not membership:
                    return Response({
                        'success': False,
                        'error': 'FORBIDDEN'
                    }, status=status.HTTP_403_FORBIDDEN)

            removed = tenant_service.remove_user_from_tenant(tenant_id, user_id)

            if removed:
                return Response({
                    'success': True,
                    'message': 'User removed from tenant',
                    'message_ar': 'تم إزالة المستخدم من المستأجر'
                })
            else:
                return Response({
                    'success': False,
                    'error': 'NOT_FOUND'
                }, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({
                'success': False,
                'error': 'VALIDATION_ERROR',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# URL patterns to add to urls.py:
# path('api/tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
# path('api/tenants/<uuid:tenant_id>/', TenantDetailView.as_view(), name='tenant-detail'),
# path('api/tenants/<uuid:tenant_id>/settings/', TenantSettingsView.as_view(), name='tenant-settings'),
# path('api/tenants/<uuid:tenant_id>/users/', TenantUsersView.as_view(), name='tenant-users'),
# path('api/tenants/<uuid:tenant_id>/users/<uuid:user_id>/', TenantUserDetailView.as_view(), name='tenant-user-detail'),
