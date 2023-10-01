from rest_framework.permissions import BasePermission


class IsActiveRequired(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        else:
            return False
