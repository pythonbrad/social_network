from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from messenger.signals import post_save_article
from messenger.signals import post_save_comment
from .user import User
from .utils import user_directory_path


class Article(models.Model):
    author = models.ForeignKey(User,
                               related_name='article_author',
                               on_delete=models.CASCADE)
    contains = models.TextField(max_length=5000)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)
    comments = models.ManyToManyField('Comment',
                                      related_name='article_comments')
    likers = models.ManyToManyField(User, related_name='article_likers')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.contains

    class Meta:
        ordering = ['date_created']

    def get_user(self):
        return self.author


class Comment(models.Model):
    author = models.ForeignKey(User,
                               related_name='comment_author',
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article,
                                related_name='article_comment',
                                on_delete=models.CASCADE)
    contains = models.TextField(max_length=5000)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)
    likers = models.ManyToManyField(User, related_name='comment_likers')
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date_created']

    def get_user(self):
        return self.author


post_save.connect(post_save_article, sender=Article)
post_save.connect(post_save_comment, sender=Comment)
