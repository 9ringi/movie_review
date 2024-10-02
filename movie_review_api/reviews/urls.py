# movie_review_api/reviews/urls.py

from django.urls import path, include
from .views import ReviewListCreateView, ReviewDetailView, MovieReviewListView, ReviewViewSet
from rest_framework.routers import DefaultRouter
from .views import MovieDetailView
from .views import MovieDetailWithReviewsView


router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('', include(router.urls)),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('movie/', MovieReviewListView.as_view(), name='movie-reviews'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<str:movie_title>/', MovieDetailWithReviewsView.as_view(), name='movie-with-reviews'),
]