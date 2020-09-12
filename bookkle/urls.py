from django.urls import path, include
from review.views import ReviewViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.contrib import admin

router = DefaultRouter(trailing_slash=False)
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^accounts', include('user.urls')),
    url(r'^reviews', include('review.urls')),
]
urlpatterns += router.urls

