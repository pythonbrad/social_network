from django.shortcuts import render
from django.shortcuts import redirect
from .account import *
from .article import *
from .friendship import *
from .message import *
from .notification import *
from .setting import *
from .user import *


def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messenger/home.html', {'title': 'Home'})
    else:
        return redirect('articles')


def panel_view(request):
    if request.user.is_authenticated:
        return render(request, 'messenger/panel.html', {
            'title': 'panel',
        })
    else:
        return redirect('login')
