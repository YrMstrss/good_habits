from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    """Проверка на то, является ли текущий пользователь пользователем, которому принадлежит объект"""
    def has_permission(self, request, view):
        return request.user == view.get_object()
