from django.db import models
from django.conf import settings
from movies.models import Movie

# Create your models here.
class Article(models.Model):
    STAR_CHOICES = ((0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), 
    (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0))
    stars = models.FloatField(choices=STAR_CHOICES)
    oneline_comment = models.TextField(max_length=30)
    content = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField(blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
