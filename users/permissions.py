from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object()
