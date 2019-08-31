from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from messenger.models import Friendship
from messenger.models import User
from .utils import build_paginator


def list_users_view(request):
    if request.user.is_authenticated:
        users = User.objects.all().exclude(pk=request.user.pk)
        users = build_paginator(request, users)[::-1]
        friends = request.user.get_list_friends(in_waiting=False)
        waiting_friends = request.user.get_list_friends(in_waiting=True)
        return render(
            request, 'messenger/list_users.html', {
                'title': _('List users'),
                'users': users,
                'friends': friends,
                'waiting_friends': waiting_friends,
            })
    else:
        return redirect('login')


def list_friends_view(request):
    if request.user.is_authenticated:
        friends = request.user.get_list_friends()
        friends = build_paginator(request, friends)[::-1]
        return render(request, 'messenger/list_friends.html', {
            'title': _('List friends'),
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


def user_details_view(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=pk)
        friends = request.user.get_list_friends()
        waiting_friends = request.user.get_list_friends(in_waiting=True)
        return render(
            request, 'messenger/user_details.html', {
                'title': _('User details'),
                'user': user,
                'friends': friends,
                'waiting_friends': waiting_friends,
                'datetime': timezone.now(),
            })
    else:
        return redirect('login')
