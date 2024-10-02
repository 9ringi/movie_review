from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'content', 'rating', 'user', 'created_at']  # Fields to include in the API
        read_only_fields = ['id', 'user', 'created_at']  # Auto-generated fields

    def validate_rating(self, value):
        """Ensure that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user