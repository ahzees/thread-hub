from rest_framework import permissions


class IsMember(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user in obj.members.all():
            return True
        
        return False