from rest_framework import permissions


class isAuthorOrReadOnly(permissions.BasePermission):
    message = "You must be the author to perform this action."
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user