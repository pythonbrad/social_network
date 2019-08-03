from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import SigninForm, LoginForm, MessageForm
from django.contrib import auth
from django.utils import timezone
from .models import Message, Friendship, User, Notification
from django.db.models import Q


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messenger/home.html', {'title': 'Home'})
    else:
        return redirect('panel')


def signin_view(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = SigninForm(request.POST)
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
            'datetime': timezone.now(),
        })
    else:
        return redirect('login')


def get_list_friendship_view(request):
    if request.user.is_authenticated:
        # Pour data frienship, use it
        friendships = Friendship.objects.filter(Q(sender=request.user)
                                                | Q(receiver=request.user),
                                                is_valided=False)
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


def get_list_users_view(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(pk=request.user.pk)
        friends = request.user.friends.all()
        waiting_friends = request.user.waiting_friends.all()
        print(users, friends)
        return render(
            request, 'messenger/list_users.html', {
                'title': 'List users',
                'users': users,
                'friends': friends,
                'waiting_friends': waiting_friends,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')


def get_list_friends_view(request):
    if request.user.is_authenticated:
        friends = request.user.friends.all()
        return render(
            request, 'messenger/list_friends.html', {
                'title': 'List friends',
                'friends': friends,
                'datetime': timezone.now(),
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
        # receiver=request.user for more security
        notification = get_object_or_404(Notification,
                                         receiver=request.user,
                                         pk=pk)
        notification.delete()
        return redirect('panel')
    else:
        return redirect('login')


def user_wall_view(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        friends = request.user.friends.all()
        return render(
            request, 'messenger/user_wall.html', {
                'title': 'User wall',
                'user': user,
                'friends': friends,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')


def send_message_view(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        if request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                if user != request.user:
                    Message.objects.create(sender=request.user,
                                       receiver=user,
                                       contains=form.cleaned_data['contains'])
                return redirect(reverse('get_messages', args=(pk, )))
        else:
            form = MessageForm()
        return render(
            request, 'messenger/send_message.html', {
                'title': 'Send message',
                'user': user,
                'datetime': timezone.now(),
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
        return render(
            request, 'messenger/get_messages.html', {
                'title': 'Messages',
                'messages': messages,
                'datetime': timezone.now(),
                'user': user,
            })


def messages_view(request):
    if request.user.is_authenticated:
        messages = request.user.messages.all()
        datas = []
        user_added = []
        for message in messages:
            if message.sender != request.user and message.sender not in user_added:
                user_added.append(message.sender)
                datas.append({
                    'user': message.sender,
                    'message': message.contains
                })
            elif message.receiver != request.user and message.receiver not in user_added:
                user_added.append(message.receiver)
                datas.append({
                    'user': message.receiver,
                    'message': message.contains
                })
            else:
                pass
        return render(
            request, 'messenger/messages.html', {
                'title': 'Messages',
                'datetime': timezone.now(),
                'datas': datas,
            })
    else:
        return redirect('login')


try:
    u1 = User.objects.create(username='fo',
                             date_of_birth='2001-05-05',
                             password='qwerty123')
    u1.is_superuser = True
    u1.is_staff = True
    u1.save()
except Exception as err:
    print(err)
