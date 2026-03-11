from rest_framework.permissions import BasePermission


class IsAdminOrOfficial(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.role in {'administrative', 'institutional'}
