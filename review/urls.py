from django.urls import path
from review.views import RandomQuoteView, RecommendToggleView, FollowingReviewView

urlpatterns = [
    path('/quote', RandomQuoteView.as_view()),
    path('/like', RecommendToggleView.as_view()),
    path('/following', FollowingReviewView.as_view()),
]
