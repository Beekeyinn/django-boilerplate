from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsOwnerOrIsAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission():
            if request.method in SAFE_METHODS:
                return True
            return (
                request.user.is_superuser
                and request.user.is_admin
                or request.user == obj.owner
            )
        return False


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission():
            if request.user == obj:
                return True
            return False
        return False
