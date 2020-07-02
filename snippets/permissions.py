from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，仅对象的拥有人可以编辑
    """

    def has_object_permission(self, request, view, obj):
        # 允许任何 request 有 Read 权限
        # 所以允许 GET, HEAD, OPTIONS 的 request
        if request.method in permissions.SAFE_METHODS:
            return True
        # 仅允许对象的创建者有 Write 权限
        return request.user == obj.owner
