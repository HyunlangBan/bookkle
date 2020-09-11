from django.urls import path, include
from review.views import ReviewViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.contrib import admin

router = DefaultRouter()
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('user.urls')),
]
urlpatterns += router.urls

