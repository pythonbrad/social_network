from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.utils import timezone
from messenger.signals import post_save_friendship
from messenger.signals import pre_delete_friendship


class Contact(models.Model):
    own = models.ForeignKey('User',
                            on_delete=models.CASCADE,
                            related_name='contact_own')
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE,
                             related_name='contact_user')
    date_last_message = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date_last_message']

    def __str__(self):
        return self.user.username


class Friendship(models.Model):
    sender = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='friendship_sender')
    receiver = models.ForeignKey('User',
                                 on_delete=models.CASCADE,
                                 related_name='friendship_receiver')
    message = models.CharField(max_length=100,
                               default="Hello, I would be your friend")
    is_valided = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return "%s and %s" % (self.sender, self.receiver)

    def get(user):
        return Friendship.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_not_valid(user):
        return Friendship.objects.filter(Q(sender=user) | Q(receiver=user),
                                         is_valided=False)

    def get_valid(user):
        return Friendship.objects.filter(Q(sender=user) | Q(receiver=user),
                                         is_valided=True)


post_save.connect(post_save_friendship, sender=Friendship)
pre_delete.connect(pre_delete_friendship, sender=Friendship)
