from django.db import models
from django.contrib.auth.models import User  # Import Django's User model

class Review(models.Model):
    movie_title = models.CharField(max_length=255)  # Title of the movie
    content = models.TextField()  # Review text
    rating = models.PositiveIntegerField()  # Rating (1 to 5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who submitted the review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created

    def __str__(self):
        return f"{self.movie_title} - {self.rating} stars"
