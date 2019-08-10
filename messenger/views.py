from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import SigninForm, LoginForm, MessageForm, ArticleForm
from django.contrib import auth
from django.utils import timezone
from .models import Message, Friendship, User, Notification, Article
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messenger/home.html', {'title': 'Home'})
    else:
        return redirect('panel')


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
        return redirect('panel')


def login_view(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                auth.login(request, user)
                return redirect('panel')
        else:
            form = LoginForm()
        return render(request, 'messenger/login.html', {
            'title': 'Login',
            'form': form
        })
    else:
        return redirect('panel')


def logout_view(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('home')


def panel_view(request):
    if request.user.is_authenticated:
        return render(request, 'messenger/panel.html', {
            'title': 'Panel',
        })
    else:
        return redirect('login')


def list_friendship_view(request):
    if request.user.is_authenticated:
        # Pour data frienship, use it
        friendships = Friendship.objects.filter(Q(sender=request.user)
                                                | Q(receiver=request.user),
                                                is_valided=False)
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
        future_friend = get_object_or_404(User, pk=pk)
        friends = request.user.friends.all()
        waiting_friends = request.user.waiting_friends.all()
        if future_friend not in friends and future_friend not in waiting_friends:
            Friendship.objects.create(sender=request.user,
                                      receiver=future_friend)
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
        friends = request.user.friends.all()
        waiting_friends = request.user.waiting_friends.all()
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
        friends = request.user.friends.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(friends, 10)
        try:
            friends = paginator.page(page)
        except PageNotAnInteger:
            friends = paginator.page(1)
        except EmptyPage:
            friends = paginator.page(paginator.num_pages)
        return render(
            request, 'messenger/list_friends.html', {
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
        redirect_to = request.GET.get('next', 'panel')
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
        friends = request.user.friends.all()
        waiting_friends = request.user.waiting_friends.all()
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
        user = get_object_or_404(User, pk=pk)
        if request.POST:
            form = MessageForm(request.POST, request.FILES)
            if form.is_valid():
                if user != request.user:
                    form.instance.sender = request.user
                    form.instance.receiver = user
                    form.save()
                return redirect(reverse('get_messages', args=(pk, )))
        else:
            form = MessageForm()
        return render(
            request, 'messenger/send_message.html', {
                'title': 'Send message',
                'user': user,
                'form': form,
            })
    else:
        return redirect('login')


def get_messages_view(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=user)
            | Q(receiver=request.user, sender=user))
        page = request.GET.get('page', 1)
        paginator = Paginator(messages, 10)
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
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
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        last_messages = []
        for user in users:
            message = Message.objects.filter(
                    Q(sender=user, receiver=request.user)
                    | Q(sender=request.user, receiver=user))
            last_messages.append({
                'user':
                user,
                'message':
                message[0] if message else [],
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
        notifications = request.user.notifications.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(notifications, 10)
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
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
        return render(
            request, 'messenger/create_article.html', {
                'title': 'Create article',
                'form': form,
            })
    else:
        return redirect('login')


def articles_view(request):
    if request.user.is_authenticated:
        articles = Article.objects.all()
        _ = []
        friends = request.user.friends.all()
        for article in articles:
            if article.author in friends or article.author == request.user:
                _.append(article)
            else:
                pass
        articles = _
        page = request.GET.get('page', 1)
        paginator = Paginator(articles, 10)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
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
        redirect_to = request.GET.get('next', 'articles')
        article = get_object_or_404(Article, author=request.user, pk=pk)
        article.delete()
        return redirect(redirect_to)
    else:
        return redirect('login')
