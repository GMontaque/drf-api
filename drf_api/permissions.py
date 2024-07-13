from rest_framework import permissions

# Define a custom permission class that inherits from BasePermission
class IsOwnerOrReadOnly(permissions.BasePermission):
    # Override the has_object_permission method to provide custom object-level permissions
    def has_object_permission(self, request, view, obj):
        # Check if the request method is in SAFE_METHODS (GET, OPTIONS, HEAD)
        if request.method in permissions.SAFE_METHODS:
            # If the method is safe, grant permission (read-only access)
            return True
        # For non-safe methods (POST, PUT, PATCH, DELETE), check if the object's owner is the same as the requesting user
        return obj.owner == request.user