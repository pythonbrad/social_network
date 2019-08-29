from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from messenger.signals import post_save_message
from messenger.signals import pre_delete_message
from .utils import user_directory_path


class Message(models.Model):
    sender = models.ForeignKey(
        'User',
        related_name='message_senders',
        on_delete=models.CASCADE,
        verbose_name=_('senders'))
    receiver = models.ForeignKey(
        'User',
        related_name='message_receivers',
        on_delete=models.CASCADE,
        verbose_name=_('receivers'))
    contains = models.TextField(
        max_length=5000,
        verbose_name=_('contains'))
    photo = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        verbose_name=_('photo'))
    received = models.BooleanField(
        default=False,
        verbose_name=_('is received?'))
    date_received = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date of reception'))
    date_created = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date of creation'))

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.contains

    def get_user(self):
        return self.sender

    def get(user1, user2):
        return Message.objects.filter(
            Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1))

    def get_new(user):
        return Message.objects.filter(Q(receiver=user), received=False)


post_save.connect(post_save_message, sender=Message)
pre_delete.connect(pre_delete_message, sender=Message)
