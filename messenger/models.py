from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from .signals import post_save_friendship
from .signals import pre_delete_friendship
from .signals import post_save_message
from .signals import pre_delete_message


# Create your models here.
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    notifications = models.ManyToManyField('Notification')
    friends = models.ManyToManyField('User', related_name='friends_list')
    waiting_friends = models.ManyToManyField(
        'User', related_name='waiting_friends_list')
    messages = models.ManyToManyField('Message')
    """
    No replace friendship, the contact save all the users
     with who a user has communicated same if this user is not his friend
    """
    contacts = models.ManyToManyField('Contact', related_name='contacts_list')
    date_created = models.DateField(default=timezone.now)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    class Meta:
        ordering = ['-date_of_birth']


class Contact(models.Model):
    own = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='contact_own')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='contact_user')
    date_last_message = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_last_message']

    def __str__(self):
        return self.user.username


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


class Message(models.Model):
    sender = models.ForeignKey(User,
                               related_name='message_sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,
                                 related_name='message_receiver',
                                 on_delete=models.CASCADE)
    contains = models.TextField(max_length=512)
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
                                 on_delete=models.CASCADE,
                                 db_constraint=False)
    message = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    obj_pk = models.IntegerField()
    url = models.URLField(blank=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-date_created']


post_save.connect(post_save_friendship, sender=Friendship)
pre_delete.connect(pre_delete_friendship, sender=Friendship)
post_save.connect(post_save_message, sender=Message)
pre_delete.connect(pre_delete_message, sender=Message)
