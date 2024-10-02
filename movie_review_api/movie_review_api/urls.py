# movie_review_api/urls.py
from django.contrib import admin
from django.urls import path, include
from reviews.views import home
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from reviews.views import UserViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('reviews.urls')),  # This line includes all other URLs from reviews.urls
]