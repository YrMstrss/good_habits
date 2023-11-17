from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверка на то, является пользователь создателем привычки
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsPublic(BasePermission):
    """Проверка - является ли привычка публичной"""
    def has_object_permission(self, request, view, obj):
        return obj.is_public
