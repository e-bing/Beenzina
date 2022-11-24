from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.core import serializers
from articles.models import Article
from movies.models import Movie

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    articles = Article.objects.filter(user_id_id=person.id)
    movies = []
    for article in articles:
        movies.append(Movie.objects.get(pk=article.movie_id))
    context = {
        'person': person,
        'articles': articles,
        'movies': movies,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                is_followed = False
            else:
                person.followers.add(user)
                is_followed = True
            followers = person.followers
            followings = person.followings
            context = {
                'is_followed': is_followed,
                # 'followers': followers,
                # 'followings': followings,
                'followers_count': followers.count(),
                'followings_count': followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:profile', person.username)
    return redirect('accounts:login')
