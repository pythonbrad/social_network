from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext as _
from messenger.models import Friendship
from .utils import build_paginator
from messenger.models import User


def list_friendship_view(request):
    if request.user.is_authenticated:
        # Pour data frienship, use it
        friendships = Friendship.get_not_valid(user=request.user)
        friendships = build_paginator(request, friendships)[::-1]
        return render(
            request, 'messenger/list_friendships.html', {
                'title': _('List friendship'),
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
