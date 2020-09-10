from django.urls import path
from user.views import SignUpView, Activate

urlpatterns = [
    path('signup/', SignUpView.as_view()),
#     path('/signin',),
     path('activate/<str:uidb64>/<str:token>', Activate.as_view())
]
