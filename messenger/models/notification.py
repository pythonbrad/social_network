from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    receiver = models.ForeignKey(
        'User',
        related_name='notification_receivers',
        on_delete=models.CASCADE,
        db_constraint=False,
        verbose_name=_('receivers'))
    message = models.CharField(
        max_length=100,
        verbose_name=_('message'))
    received = models.BooleanField(
        default=False,
        verbose_name=_('is received?'))
    date_created = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date of creation'))
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
