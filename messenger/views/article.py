from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from messenger.models import Article
from messenger.models import Comment
from messenger.forms import ArticleForm
from messenger.forms import CommentForm
from .utils import build_paginator


def create_article_view(request):
    if request.user.is_authenticated:
        if request.POST:
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect('articles')
        else:
            form = ArticleForm()
        return render(request, 'messenger/create_article.html', {
            'title': _('Create article'),
            'form': form,
        })
    else:
        return redirect('login')


def articles_view(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()
        result = []
        friends = request.user.get_list_friends()
        for article in articles:
            if article.author in friends or article.author == request.user:
                result.append(article)
            else:
                pass
        articles = result
        articles = build_paginator(request, articles)[::-1]
        return render(
            request, 'messenger/articles.html', {
                'title': _('Articles'),
                'datetime': timezone.now(),
                'articles': articles,
            })
    else:
        return redirect('login')


def delete_article_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        # author=request.user for more security
        article = get_object_or_404(Article, author=request.user, pk=pk)
        article.delete()
        return redirect(redirect_to)
    else:
        return redirect('login')


def liked_article_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'articles')
        article = get_object_or_404(Article, pk=pk)
        if request.user in article.likers.all():
            article.likers.remove(request.user)
        else:
            article.likers.add(request.user)
        return redirect(redirect_to)
    else:
        return redirect('login')


def create_comment_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        article = get_object_or_404(Article, pk=pk)
        if request.POST:
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.article = article
                form.instance.author = request.user
                form.save()
                return redirect(redirect_to)
        else:
            form = CommentForm()
        return render(
            request, 'messenger/create_comment.html', {
                'title': _('Create comment'),
                'form': form,
                'article': article,
                'redirect_to': redirect_to,
            })
    else:
        return redirect('login')


def get_comments_view(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comments = article.comments.all()
        comments = build_paginator(request, comments)[::-1]
        return render(
            request, 'messenger/get_comments.html', {
                'title': _('Comments'),
                'comments': comments,
                'article': article,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')


def delete_comment_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        # author=request.user for more security
        comment = get_object_or_404(Comment, author=request.user, pk=pk)
        comment.delete()
        return redirect(redirect_to)
    else:
        return redirect('login')


def liked_comment_view(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=pk)
        redirect_to = request.GET.get(
            'next', reverse('get_comments', args=(comment.article.pk, )))
        if request.user in comment.likers.all():
            comment.likers.remove(request.user)
        else:
            comment.likers.add(request.user)
        return redirect(redirect_to)
    else:
        return redirect('login')


def share_article_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        article = get_object_or_404(Article, pk=pk)
        article.share(request.user)
        return redirect(redirect_to)
    else:
        return redirect('login')
