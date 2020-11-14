from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.CharField(max_length = 10, primary_key=True)
    title = models.CharField(max_length = 100)
    is_adult = models.BooleanField()
    year = models.DateField()
    runtime = models.IntegerField()

class MovieGenre(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.CharField(max_length = 100)

class MovieRatings(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    average_rating = models.DecimalField(max_digits = 3, decimal_places = 1)
    num_votes = models.IntegerField()