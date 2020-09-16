from django.urls import path
from review.views import RandomQuoteView, RecommendView

urlpatterns = [
    path('/quote', RandomQuoteView.as_view()),
    path('/like', RecommendView.as_view()),
]
