from django.urls import path

from user.views import (
        SignUpView, 
        LogoutView,
        Activate, 
        LoginView, 
        MyReviewView, 
        UserProfileView, 
        FollowToggleView
)

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin',LoginView.as_view()),
    path('/signout', LogoutView.as_view()),
    path('/activate/<str:uidb64>/<str:token>', Activate.as_view()),
    path('/my-reviews/<int:pk>', MyReviewView.as_view()),
    path('/profile/<int:pk>', UserProfileView.as_view()),
    path('/follow', FollowToggleView.as_view()),
]
