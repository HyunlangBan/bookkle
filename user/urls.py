from django.urls import path
from user.views import SignUpView, Activate, LoginView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('signin',LoginView.as_view()),
    path('activate/<str:uidb64>/<str:token>', Activate.as_view())
]
