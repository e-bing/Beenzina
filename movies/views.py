from django.views.decorators.http import require_safe
from django.shortcuts import render
from .models import Movie
from articles.models import Article
from movies.models import Genre

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
        }
    return render(request, 'movies/index.html', context)

def detail(request,movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    articles = Article.objects.filter(movie_id=movie_pk)
    genres = []
    for genre_id in movie.genres:
        genres.append(Genre.objects.get(num=genre_id))

    context = {
        'movie' : movie,
        'articles' : articles,
        'genres' : genres,
    }
    return render(request, 'movies/detail.html', context)
