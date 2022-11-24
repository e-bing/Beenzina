from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from movies.models import Movie

# Create your views here.
@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    movies = Movie.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user_id = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(
        )
    context = {
        'form': form,
        'user': request.user,
        'movies': movies,
    }
    return render(request, 'articles/create.html', context)

@require_GET
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    movie = get_object_or_404(Movie, pk=article.movie_id)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'user': request.user,
        'comment_form': comment_form,
        'comments': comments,
        'movie': movie,
    }
    return render(request, 'articles/detail.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.user == article.user_id:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)

@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)
        if request.user == article.user_id:
            article.delete()
            return redirect('accounts:profile', request.user)
    return redirect('articles:detail', article.pk)


@require_POST
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user_id = request.user.id
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'comment_form': comment_form,
        'article': article,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', context)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)
