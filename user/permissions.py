from rest_framework import permissions

class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or 
            request.user and request.user.is_authenticated
        )
        

    # 로그인 안했을때 리뷰 리스트 보이도록 하기
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and
            obj.user == request.user)
        )

