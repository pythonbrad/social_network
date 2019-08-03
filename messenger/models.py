from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from .signals import post_create_friendship
from .signals import post_delete_friendship
from .signals import post_create_message
from .signals import post_delete_message


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField()
    notifications = models.ManyToManyField('Notification',
                                           related_name='user_notification')
    is_group = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['date_of_birth']

    class Meta:
        ordering = ['-date_of_birth']


class Friendship(models.Model):
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='friendship_sender')
    receiver = models.ForeignKey(User,
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

    def get_list_friends(user):
        friendships = Friendship.objects.filter(Q(receiver=user)
                                                | Q(sender=user),
                                                is_valided=True)
        friends_list = []
        for friendship in friendships:
            if friendship.sender != user:
                friends_list.append(friendship.sender)
            elif friendship.receiver != user:
                friends_list.append(friendship.receiver)
            else:
                pass
        return friends_list

    def get_list_all_friends(user):
        friendships = Friendship.objects.filter(
            Q(receiver=user)
            | Q(sender=user))
        friends_list = []
        for friendship in friendships:
            if friendship.sender != user:
                friends_list.append(friendship.sender)
            elif friendship.receiver != user:
                friends_list.append(friendship.receiver)
            else:
                pass
        return friends_list


class Message(models.Model):
    sender = models.ForeignKey(User,
                               related_name='message_sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,
                                 related_name='message_receiver',
                                 on_delete=models.CASCADE)
    contains = models.CharField(max_length=512)
    seen = models.BooleanField(default=False)
    date_received = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.contains


class Notification(models.Model):
    receiver = models.ForeignKey(User,
                                 related_name='notification_receiver',
                                 on_delete=models.CASCADE)
    message = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    obj_pk = models.IntegerField()

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-date_created']


post_save.connect(post_create_friendship, sender=Friendship)
post_delete.connect(post_delete_friendship, sender=Friendship)
post_save.connect(post_create_message, sender=Message)
post_delete.connect(post_delete_message, sender=Message)
