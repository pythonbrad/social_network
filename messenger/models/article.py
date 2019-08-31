from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from messenger.signals import post_save_article
from messenger.signals import post_save_comment
from .user import User
from .utils import user_directory_path


class Article(models.Model):
    author = models.ForeignKey(User,
                               related_name='article_authors',
                               on_delete=models.CASCADE,
                               verbose_name=_('authors'))
    contains = models.TextField(max_length=5000, verbose_name=_('contains'))
    photo = models.ImageField(upload_to=user_directory_path,
                              blank=True,
                              verbose_name='photo')
    comments = models.ManyToManyField('Comment',
                                      related_name='article_comments',
                                      verbose_name=_('comments'))
    likers = models.ManyToManyField(User,
                                    related_name='article_likers',
                                    verbose_name=_('likers'))
    date_created = models.DateTimeField(default=timezone.now,
                                        verbose_name=_('date of creation'))

    def __str__(self):
        return self.contains

    class Meta:
        ordering = ['date_created']

    def get_user(self):
        return self.author

    def share(self, user):
        backup_language = translation.get_language()
        for friend in user.get_list_friends():
            # set language of receiver of notification
            translation.activate(friend.language)
            friend.create_notification(message=_(
                "%(user1)s said: Can you see this article of %(user2)s?") % {
                    'user1': user.username,
                    'user2': self.author.username
                },
                                       url=reverse('get_comments',
                                                   args=(self.pk, )),
                                       obj_pk=self.pk)
        # Restore the language
        translation.activate(backup_language)

    def make_notification(author, contains, photo):
        Article.objects.create(author=author, contains=contains, photo=photo)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               related_name='comment_authors',
                               on_delete=models.CASCADE,
                               verbose_name=_('authors'))
    article = models.ForeignKey(Article,
                                related_name='commented_article',
                                on_delete=models.CASCADE,
                                verbose_name=_('article'))
    contains = models.TextField(max_length=5000, verbose_name=_('contains'))
    photo = models.ImageField(upload_to=user_directory_path,
                              blank=True,
                              verbose_name=_('photo'))
    likers = models.ManyToManyField(User,
                                    related_name='comment_likers',
                                    verbose_name=_('likers'))
    date_created = models.DateTimeField(default=timezone.now,
                                        verbose_name=_('date of creation'))

    class Meta:
        ordering = ['date_created']

    def get_user(self):
        return self.author


post_save.connect(post_save_article, sender=Article)
post_save.connect(post_save_comment, sender=Comment)
