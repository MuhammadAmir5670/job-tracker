from rest_framework import permissions


class TechStackPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated for list and view actions
        if view.action == 'list':
            return request.user.is_authenticated and request.user.has_perm('jobs.view_techstack')
        elif view.action == 'create':
            return request.user.is_authenticated and request.user.has_perm('jobs.add_techstack')
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return request.user.is_authenticated and request.user.has_perm('jobs.change_techstack')
        elif view.action == 'destroy':
            return request.user.is_authenticated and request.user.has_perm('jobs.delete_techstack')
        return False
