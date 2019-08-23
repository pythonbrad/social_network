from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import SigninForm, LoginForm, MessageForm, ArticleForm, CommentForm
from django.contrib import auth
from django.utils import timezone
from .models import Message, Friendship, User, Notification, Article, Comment
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messenger/home.html', {'title': 'Home'})
    else:
        return redirect('articles')


def signin_view(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = SigninForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SigninForm()
        return render(request, 'messenger/signin.html', {
            'title': 'Signin',
            'form': form,
        })
    else:
        return redirect('home')


def login_view(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                auth.login(request, user)
                return redirect('home')
        else:
            form = LoginForm()
        return render(request, 'messenger/login.html', {
            'title': 'Login',
            'form': form
        })
    else:
        return redirect('home')


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')


def panel_view(request):
    if request.user.is_authenticated:
        return render(request, 'messenger/panel.html', {
            'title': 'panel',
        })
    else:
        return redirect('login')


def list_friendship_view(request):
    if request.user.is_authenticated:
        # Pour data frienship, use it
        friendships = Friendship.get_not_valid(user=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(friendships, 10)
        try:
            friendships = paginator.page(page)
        except PageNotAnInteger:
            friendships = paginator.page(1)
        except EmptyPage:
            friendships = paginator.page(paginator.num_pages)
        return render(
            request, 'messenger/list_friendships.html', {
                'title': 'List friendship',
                'friendships': friendships,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')


def create_friendship_view(request, pk):
    if request.user.is_authenticated:
        if request.user.pk != pk:
            future_friend = get_object_or_404(User, pk=pk)
            friends = request.user.get_list_friends(in_waiting=None)
            if future_friend in friends:
                pass
            else:
                Friendship.objects.create(sender=request.user,
                                          receiver=future_friend)
        else:
            pass
        return redirect('list_users')
    else:
        return redirect('login')


def delete_friendship_view(request, pk):
    if request.user.is_authenticated:
        friendship = get_object_or_404(Friendship,
                                       Q(receiver=request.user)
                                       | Q(sender=request.user),
                                       pk=pk)
        friendship.delete()
        return redirect('list_friendships')
    else:
        return redirect('login')


def accept_friendship_view(request, pk):
    if request.user.is_authenticated:
        friendship = get_object_or_404(Friendship,
                                       receiver=request.user,
                                       pk=pk)
        friendship.is_valided = True
        friendship.save()
        return redirect('list_friendships')
    else:
        return redirect('login')


def list_users_view(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(pk=request.user.pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        friends = request.user.get_list_friends(in_waiting=False)
        waiting_friends = request.user.get_list_friends(in_waiting=True)
        return render(
            request, 'messenger/list_users.html', {
                'title': 'List users',
                'users': users,
                'friends': friends,
                'waiting_friends': waiting_friends,
            })
    else:
        return redirect('login')


def list_friends_view(request):
    if request.user.is_authenticated:
        friends = request.user.get_list_friends()
        page = request.GET.get('page', 1)
        paginator = Paginator(friends, 10)
        try:
            friends = paginator.page(page)
        except PageNotAnInteger:
            friends = paginator.page(1)
        except EmptyPage:
            friends = paginator.page(paginator.num_pages)
        return render(request, 'messenger/list_friends.html', {
            'title': 'List friends',
            'friends': friends,
        })
    else:
        return redirect('login')


def delete_friend_view(request, pk):
    if request.user.is_authenticated:
        friend = get_object_or_404(User, pk=pk)
        friendship = get_object_or_404(
            Friendship,
            Q(receiver=request.user, sender=friend)
            | Q(sender=request.user, receiver=friend))
        friendship.delete()
        return redirect('list_friends')
    else:
        return redirect('login')


def delete_notification_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        # receiver=request.user for more security
        notification = get_object_or_404(Notification,
                                         receiver=request.user,
                                         pk=pk)
        notification.delete()
        return redirect(redirect_to)
    else:
        return redirect('login')


def user_details_view(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        friends = request.user.get_list_friends()
        waiting_friends = request.user.get_list_friends(in_waiting=True)
        return render(
            request, 'messenger/user_details.html', {
                'title': 'User details',
                'user': user,
                'friends': friends,
                'waiting_friends': waiting_friends,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')


def send_message_view(request, pk):
    if request.user.is_authenticated:
        if request.user.pk != pk:
            user = get_object_or_404(User, pk=pk)
            if request.POST:
                form = MessageForm(request.POST, request.FILES)
                if form.is_valid():
                    form.instance.sender = request.user
                    form.instance.receiver = user
                    form.save()
                    return redirect(reverse('get_messages', args=(pk, )))
            else:
                form = MessageForm()
            return render(request, 'messenger/send_message.html', {
                'title': 'Send message',
                'user': user,
                'form': form,
            })
        else:
            return redirect('home')
    else:
        return redirect('login')


def get_messages_view(request, pk):
    if request.user.is_authenticated:
        if request.user.pk != pk:
            user = get_object_or_404(User, pk=pk)
            messages = Message.get(user1=user, user2=request.user)
            page = request.GET.get('page', None)
            paginator = Paginator(messages, 10)
            try:
                messages = paginator.page(page)
            except PageNotAnInteger:
                last_page = paginator.page_range[-1]
                messages = paginator.page(last_page)
            except EmptyPage:
                messages = paginator.page(paginator.num_pages)
            for message in messages:
                if not message.received and message.receiver == request.user:
                    message.received = True
                    message.date_received = timezone.now()
                    message.save()
            return render(
                request, 'messenger/get_messages.html', {
                    'title': 'Messages',
                    'messages': messages,
                    'datetime': timezone.now(),
                    'user': user,
                })
        else:
            return redirect('home')
    else:
        return redirect('login')


def delete_message_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'messages')
        # receiver=request.user for more security
        message = get_object_or_404(Message, sender=request.user, pk=pk)
        message.delete()
        return redirect(redirect_to)
    else:
        return redirect('login')


def messages_view(request):
    if request.user.is_authenticated:
        users = [contact.user for contact in request.user.contacts.all()]
        page = request.GET.get('page', None)
        paginator = Paginator(users, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            last_page = paginator.page_range[-1]
            users = paginator.page(last_page)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        last_messages = []
        for user in users:
            message = Message.get(user1=user, user2=request.user)
            last_messages.append({
                'user': user,
                'message': message.last() if message else [],
            })
        return render(
            request, 'messenger/messages.html', {
                'title': 'Messages',
                'datetime': timezone.now(),
                'users': users,
                'last_messages': last_messages,
            })
    else:
        return redirect('login')


def list_notifications_view(request):
    if request.user.is_authenticated:
        notifications = Notification.get(user=request.user)
        page = request.GET.get('page', None)
        paginator = Paginator(notifications, 10)
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            last_page = paginator.page_range[-1]
            notifications = paginator.page(last_page)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        for notification in notifications:
            if not notification.received:
                notification.received = True
                notification.save()
        return render(
            request, 'messenger/notifications.html', {
                'title': 'Notifications',
                'datetime': timezone.now(),
                'notifications': notifications,
            })
    else:
        return redirect('login')


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
            'title': 'Create article',
            'form': form,
        })
    else:
        return redirect('login')


def articles_view(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()
        _ = []
        friends = request.user.get_list_friends()
        for article in articles:
            if article.author in friends or article.author == request.user:
                _.append(article)
            else:
                pass
        articles = _
        page = request.GET.get('page', None)
        paginator = Paginator(articles, 10)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            last_page = paginator.page_range[-1]
            articles = paginator.page(last_page)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return render(
            request, 'messenger/articles.html', {
                'title': 'Articles',
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
                'title': 'Create comment',
                'form': form,
                'article': article,
                'redirect_to': redirect_to,
            })
    else:
        return redirect('login')


def get_comments_view(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        page = request.GET.get('page', None)
        comments = article.comments.all()
        paginator = Paginator(comments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            last_page = paginator.page_range[-1]
            comments = paginator.page(last_page)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        return render(
            request, 'messenger/get_comments.html', {
                'title': 'Comments',
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


def share_article_view(request, pk):
    if request.user.is_authenticated:
        redirect_to = request.GET.get('next', 'home')
        article = get_object_or_404(Article, pk=pk)
        for friend in request.user.get_list_friends():
            Notification.objects.create(
                receiver=friend,
                message="%s said: Can you see this article of %s?" %
                (request.user.username, article.author.username),
                url=reverse('get_comments', args=(pk, )),
                obj_pk=pk)
        return redirect(redirect_to)
    else:
        return redirect('login')
