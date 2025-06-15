from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "You must be permitted to perform this action."
    
    def has_permission(self, request, view):
        # 调试打印（实际生产环境可以去掉）
        print(f"Checking permission for {request.method} request")
        
        # 允许所有安全方法（GET, HEAD, OPTIONS）
        if request.method in permissions.SAFE_METHODS:
            print("Safe method allowed")
            return True
            
        # 对于非安全方法，要求用户是超级用户
        print(f"User is staff: {request.user.is_staff}")
        return request.user.is_staff