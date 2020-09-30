# https://www.django-rest-framework.org/api-guide/permissions/
# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
from rest_framework.permissions import BasePermission

# has_permission : for list or another ( /rooms/ )
# has_object_permission : for detail view ( /room/1 ) only call for object

# has_object_permission이 알맞음
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, room):
        return room.user == request.user
