from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from messenger.models import Message
from messenger.models import User
from messenger.forms import MessageForm
from .utils import build_paginator


def send_message_view(request, pk):
    if request.user.is_authenticated:
        if request.user.pk != pk:
            user = get_object_or_404(User, pk=pk)
            if request.POST:
                form = MessageForm(request.POST, request.FILES)
                if form.is_valid():
                    form.instance.sender = request.user
                    form.instance.receiver = user
                    form.save()
                    return redirect(reverse('get_messages', args=(pk, )))
            else:
                form = MessageForm()
            return render(request, 'messenger/send_message.html', {
                'title': 'Send message',
                'user': user,
                'form': form,
            })
        else:
            return redirect('home')
    else:
        return redirect('login')


def get_messages_view(request, pk):
    if request.user.is_authenticated:
        if request.user.pk != pk:
            user = get_object_or_404(User, pk=pk)
            messages = Message.get(user1=user, user2=request.user)
            messages = build_paginator(request, messages)
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
            return redirect('home')
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
        users = build_paginator(request, users)
        last_messages = []
        for user in users:
            message = Message.get(user1=user, user2=request.user)
            last_messages.append({
                'user': user,
                'message': message.last() if message else [],
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
