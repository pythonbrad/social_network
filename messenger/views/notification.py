from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from messenger.models import Notification
from .utils import build_paginator


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


def list_notifications_view(request):
    if request.user.is_authenticated:
        notifications = Notification.get(user=request.user)
        notifications = build_paginator(request, notifications)
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
