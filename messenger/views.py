from django.shortcuts import render, redirect, get_object_or_404
from .forms import SigninForm, LoginForm, MessageForm
from django.contrib import auth
from .models import Message, Friendship, User
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
        })
    else:
        return redirect('login')


def get_list_friendship_view(request):
    if request.user.is_authenticated:
        friendships = Friendship.objects.filter(Q(sender=request.user)
                                                | Q(receiver=request.user),
                                                is_valided=False)
        return render(request, 'messenger/list_friendship.html', {
            'title': 'List friendship',
            'friendships': friendships,
        })
    else:
        return redirect('login')


def create_friendship_view(request, pk):
    if request.user.is_authenticated:
        receiver = get_object_or_404(User, pk=pk)
        friendship = Friendship.objects.filter(
            Q(receiver=request.user, sender=receiver)
            | Q(sender=request.user, receiver=receiver))
        if not friendship:
            Friendship.objects.create(sender=request.user, receiver=receiver)
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
        return redirect('list_friendship')
    else:
        return redirect('login')


def accept_friendship_view(request, pk):
    if request.user.is_authenticated:
        friendship = get_object_or_404(Friendship,
                                       Q(receiver=request.user)
                                       | Q(sender=request.user),
                                       pk=pk)
        friendship.is_valided = True
        friendship.save()
        return redirect('list_friendship')
    else:
        return redirect('login')


def get_list_users_view(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(pk=request.user.pk)
        return render(request, 'messenger/list_users.html', {
            'title': 'List users',
            'users': users,
        })
    else:
        return redirect('login')


def get_list_friends_view(request):
    if request.user.is_authenticated:
        # Dont user request.user.friend because
        # it contains the user not whom the frienship is not valided
        friendships = Friendship.objects.filter(
            Q(receiver=request.user)
            | Q(sender=request.user), is_valided=True)
        all_friends = request.user.friends.all()
        friends_valided = []
        for friendship in friendships:
            if friendship.sender in all_friends:
                friends_valided.append(friendship.sender)
            elif friendship.receiver in all_friends:
                friends_valided.append(friendship.receiver)
            else:
                pass
        return render(request, 'messenger/list_friends.html', {
            'title': 'List friends',
            'friends': friends_valided,
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


try:
    u1 = User.objects.create(username='fo',
                             date_of_birth='2001-05-05',
                             password='qwerty123')
    u1.is_superuser = True
    u1.is_staff = True
    u1.save()
except Exception as err:
    print(err)
