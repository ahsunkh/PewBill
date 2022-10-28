from rest_framework.permissions import BasePermission

from loginAndRegister.models import Users


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        try:
            id = (request.user.token.get('id', None))
            user = Users.get_user_by_id(id=id)
            if user.role_id == 1:  # for admin permission id admin = 1
                return True
            else:
                return False
        except Exception as err:
            return False