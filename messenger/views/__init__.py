from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .account import *
from .article import *
from .friendship import *
from .message import *
from .notification import *
from .setting import *
from .user import *


def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'messenger/home.html', {'title': _('Home')})
    else:
        return redirect('articles')


def panel_view(request):
    if request.user.is_authenticated:
        return render(request, 'messenger/panel.html', {
            'title': _('Panel'),
        })
    else:
        return redirect('login')
