from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import DONE

class IsAuthenticatedAndDone(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.status == DONE
    

class IsAuthenticatedAndAutor(BasePermission):
     def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.status == DONE
     
     def has_object_permission(self, request, view, obj):
         return obj.user == request.user


class IsAuthenticatedAndAutorForMedia(BasePermission):
     def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.status == DONE
     
     def has_object_permission(self, request, view, obj):
         return obj.post.user == request.user
