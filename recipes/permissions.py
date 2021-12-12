from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
    # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the author of a post
        return obj.author == request.user


class IsAdminOrUserOrReadOnly(permissions.BasePermission):

    # user can only view endpoint if authenticated/logged in
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
    # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        # Write permissions are only allowed to the owner of username
        return obj.username == request.user.username