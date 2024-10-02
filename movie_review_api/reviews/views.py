from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from reviews.serializers import UserSerializer
from reviews.serializers import ReviewSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.conf import settings
from rest_framework.views import APIView
import requests
from rest_framework import status




def home(request):
    return HttpResponse("Welcome to the Movie Review API!")


# List all reviews or create a new review
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can create reviews

    def perform_create(self, serializer):
        # Set the user who created the review automatically
        serializer.save(user=self.request.user)

# Retrieve, update, or delete a specific review
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Ensure the review's owner is the one making the update
        if self.get_object().user != self.request.user:
            raise PermissionError("You can only update your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only the review owner can delete the review
        if instance.user != self.request.user:
            raise PermissionError("You can only delete your own reviews.")
        instance.delete()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the review
        return obj.user == request.user
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

        # Add filtering and pagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['movie_title']  # Allows filtering by movie title
    ordering_fields = ['created_at', 'rating']  # Allow ordering by these fields
    ordering = ['created_at']  # Default ordering

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewFilter(filters.FilterSet):
    movie_title = filters.CharFilter(field_name='movie_title', lookup_expr='icontains')
    rating = filters.NumberFilter(field_name='rating')


    class Meta:
        model = Review
        fields = ['movie_title', 'rating']

class MovieReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = ReviewFilter
    ordering_fields = ['created_at', 'rating']  # Define fields to order by
    ordering = ['-created_at']  # Default ordering

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={settings.TMDB_API_KEY}'
        response = requests.get(url)
        
        if response.status_code == 200:
            movie_data = response.json()
            return Response(movie_data)
        else:
            return Response({"detail": "Movie not found."}, status=404)

class MovieDetailWithReviewsView(APIView):
    def get(self, request, movie_title):
        # Fetch movie details from TMDB
        tmdb_api_key = settings.TMDB_API_KEY
        movie_response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={movie_title}')
        
        if movie_response.status_code != 200:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        movie_data = movie_response.json().get('results')
        if not movie_data:
            return Response({'error': 'No movie found'}, status=status.HTTP_404_NOT_FOUND)

        movie_details = movie_data[0]  # Assuming first result is the desired one
        movie_id = movie_details.get('id')

        # Fetch associated reviews
        reviews = Review.objects.filter(movie_title=movie_details.get('title'))
        review_serializer = ReviewSerializer(reviews, many=True)

        response_data = {
            'movie_details': {
                'id': movie_details.get('id'),
                'title': movie_details.get('title'),
                'overview': movie_details.get('overview'),
                'release_date': movie_details.get('release_date'),
                'rating': movie_details.get('vote_average'),
            },
            'reviews': review_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
