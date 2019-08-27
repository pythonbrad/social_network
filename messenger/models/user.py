from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .utils import user_directory_path
from .notification import Notification
from .relationship import Friendship
from .message import Message


class User(AbstractUser):
    username = models.CharField(max_length=50, primary_key=True)
    date_of_birth = models.DateField()
    email = models.EmailField()
    photo = models.ImageField(upload_to=user_directory_path,
                              blank=True,
                              default='no_image.png')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    """
    No replace friendship, the contact save all the users
     with who a user has communicated same if this user is not his friend
    """
    contacts = models.ManyToManyField('Contact', related_name='contacts_list')
    no_media = models.BooleanField(default=False)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    def __str__(self):
        return self.username

    def get_user(self):
        return self

    def get_state(self):
        new_notifications = Notification.get_new(user=self)
        waiting_friends = Friendship.get_not_valid(user=self)
        new_messages = Message.get_new(user=self)
        return locals()

    def get_list_friends(self, in_waiting=False):
        if in_waiting is not None:
            if in_waiting:
                friendships = Friendship.get_not_valid(self)
            else:
                friendships = Friendship.get_valid(self)
        else:
            friendships = Friendship.get(self)
        friends = []
        for friendship in friendships:
            if friendship.sender != self:
                friends.append(friendship.sender)
            else:
                friends.append(friendship.receiver)
        return friends

    def create_notification(self, message, obj_pk, url):
        return Notification.objects.create(receiver=self,
                                           message=message,
                                           obj_pk=obj_pk,
                                           url=url)

    def get_notification(self, obj_pk):
        return Notification.objects.filter(obj_pk=obj_pk)