from rest_framework import permissions

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            # return request.user.is_authenticated
            return True
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return True
        elif view.action == 'destroy':
            return bool(request.user.is_superuser)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            print(obj.username)
            return obj.username == request.user.username or request.user.is_staff
        elif view.action == 'destroy':
            return bool(request.user.is_staff)
        else:
            return False

        # admin : del , PUT , POST
        # user :  GET , PUT

