from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
"""TO USED
class MyUser(AbstractBaseUser):
    ...
    date_of_birth = models.DateField()
    height = models.FloatField()
    ...
    REQUIRED_FIELDS = ['date_of_birth', 'height']
"""


class Message(models.Model):
    own = models.ForeignKey(User,
                            related_name='message_own',
                            on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,
                                 related_name='message_receiver',
                                 on_delete=models.CASCADE)
    contains = models.CharField(max_length=50)
    received = models.BooleanField(default=False)
    date_received = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        c = self.contains
        if len(c) > 20:
            c = c[:20] + '...'
        return c
