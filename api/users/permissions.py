from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj == request.user


class IsPatient(permissions.BasePermission):
    """
    Permission class to check if user is a patient
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient


class IsDoctor(permissions.BasePermission):
    """
    Permission class to check if user is a doctor
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user is an admin
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsDoctorOrPatient(permissions.BasePermission):
    """
    Permission class to check if user is either a doctor or patient
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_doctor or request.user.is_patient)
