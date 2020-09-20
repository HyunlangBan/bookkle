from django.urls import path
from review.views import RandomQuoteView, RecommendToggleView, FollowingReviewView

urlpatterns = [
    path('/quote', RandomQuoteView.as_view(), name='random-quote'),
    path('/like', RecommendToggleView.as_view(), name='like'),
    path('/following', FollowingReviewView.as_view(), name='following'),
]
