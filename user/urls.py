from django.urls import path

from user.views import (
        SignUpView, 
        Activate, 
        LoginView, 
        MyReviewView, 
        UserProfileView, 
        FollowToggleView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin',LoginView.as_view()),
    path('/activate/<str:uidb64>/<str:token>', Activate.as_view()),
    path('/my-reviews/<int:pk>', MyReviewView.as_view(), name='my-reviews'),
    path('/profile/<int:pk>', UserProfileView.as_view(), name='user-profile'),
    path('/follow', FollowToggleView.as_view(), name='follow'),
]
