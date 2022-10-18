from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_superuser
            and request.user.is_admin
            or request.user == obj.owner
        )
