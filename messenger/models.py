from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField()
    friends = models.ManyToManyField('User',
                                     related_name='user_friends',
                                     through='Friendship')
    is_group = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['date_of_birth']


class Friendship(models.Model):
    sender = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='friendship_sender')
    receiver = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='friendship_receiver')
    message = models.CharField(max_length=100, default="Hello, I would be your friend")
    is_valided = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    own = models.ForeignKey(User,
                            related_name='message_own',
                            on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,
                                 related_name='message_receiver',
                                 on_delete=models.CASCADE)
    contains = models.CharField(max_length=50)
    seen = models.BooleanField(default=False)
    date_received = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        c = self.contains
        if len(c) > 20:
            c = c[:20] + '...'
        return c


class Notification(models.Model):
    receiver = models.ForeignKey(User,
                                 related_name='notification_receiver',
                                 on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        c = self.message
        if len(c) > 20:
            c = c[:20] + '...'
        return c
