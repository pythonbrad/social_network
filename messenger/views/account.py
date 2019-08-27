from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from messenger.forms import SigninForm
from messenger.forms import LoginForm


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
