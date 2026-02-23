from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''Custom permission to only allow owners of an object to edit it.'''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the project.
        return obj.owner == request.user


class IsMember(permissions.BasePermission):
    '''Custom permission to only allow members of a project to access it.'''

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if hasattr(obj, 'members'):
            project = obj.project
            if project is None:
                return obj.user == request.user
            else:
                return project.owner == request.user or request.user in project.members.all()
        else:
            return obj.owner == request.user or request.user in obj.members.all()
