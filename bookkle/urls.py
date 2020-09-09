from django.urls import path, include
from review.views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'review', ReviewViewSet, basename='review')
urlpatterns = router.urls

