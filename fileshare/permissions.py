from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'ops'

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'client' and request.user.is_verified
