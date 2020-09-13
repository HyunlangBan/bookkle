from django.urls import path
from review.views import RandomQuoteView

urlpatterns = [
    path('/quote', RandomQuoteView.as_view()),
]
