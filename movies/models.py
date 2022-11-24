from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=20)
    genres = models.JSONField()
    released_date = models.DateField()
    popularity = models.FloatField()
    vote_average = models.FloatField()
    poster_path = models.TextField()
    overview = models.TextField()

    def __str__(self):
        return self.title

class Genre(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=20)
