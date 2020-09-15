from django.urls import path
from review.views import RandomQuoteView, LikeView

urlpatterns = [
    path('/quote', RandomQuoteView.as_view()),
    path('/like', LikeView.as_view()),
]
