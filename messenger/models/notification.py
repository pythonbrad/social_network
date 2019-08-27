from django.db import models
from django.db.models import Q
from django.utils import timezone


class Notification(models.Model):
    receiver = models.ForeignKey('User',
                                 related_name='notification_receiver',
                                 on_delete=models.CASCADE,
                                 db_constraint=False)
    message = models.CharField(max_length=100)
    received = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    obj_pk = models.IntegerField()
    url = models.URLField(blank=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['date_created']

    def get_new(user):
        return Notification.objects.filter(receiver=user, received=False)

    def get(user):
        return Notification.objects.filter(Q(receiver=user))
