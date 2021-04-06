from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.permissions import BasePermission, AllowAny


class ActionBasedPermission(BasePermission):

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                klass_i = klass()
                return klass_i.has_permission(request, view)
                # if isinstance(klass_i, AllowAny) or request.user.is_authenticated:
                # raise AuthenticationFailed() if request.headers.get('authorization') else NotAuthenticated()
        return False
