from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils import translation


def post_save_friendship(sender, instance, created, **kwargs):
    # Backup of user actual language
    backup_language = translation.get_language()

    if created:
        # Translate in notification receiver language
        translation.activate(instance.receiver.language)
        instance.receiver.create_notification(
            message=_('%(user)s said "Hello, I would be your friend"') % {
                'user': instance.sender,
            },
            obj_pk=instance.pk,
            url=reverse('list_friendships'),
        )

    else:
        if instance.is_valided:
            # Translate in notification receiver language
            translation.activate(instance.sender.language)
            instance.sender.create_notification(
                message=_('%(user)s has accepted your friendship') %
                {'user': instance.receiver},
                obj_pk=instance.pk,
                url=reverse('user_details', args=(instance.receiver.pk, )),
            )

            for friend in instance.sender.get_list_friends():
                # Translate in notification receiver language
                translation.activate(friend.language)
                friend.create_notification(
                    message=_("%(user1)s is now in friendship with %(user2)s")
                    % {
                        'user1': instance.sender,
                        'user2': instance.receiver
                    },
                    obj_pk=instance.pk,
                    url=reverse('user_details', args=(instance.receiver, )))
            for friend in instance.receiver.get_list_friends():
                # Translate in notification receiver language
                translation.activate(friend.language)
                friend.create_notification(
                    message=_("%(user1)s is now in friendship with %(user2)s")
                    % {
                        'user1': instance.receiver,
                        'user2': instance.sender
                    },
                    obj_pk=instance.pk,
                    url=reverse('user_details', args=(instance.sender, )))

        else:
            pass
    # Restore the language backup
    translation.activate(backup_language)


def pre_delete_friendship(sender, instance, **kwargs):
    notifications = instance.receiver.get_notification(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()

    # Backup of user actual language
    backup_language = translation.get_language()

    if instance.is_valided:
        # Translate in notification receiver language
        translation.activate(instance.receiver.language)
        instance.receiver.create_notification(
            message=_('your friendship with %(user)s has been canceled') %
            {'user': instance.sender},
            url=reverse('user_details', args=(instance.sender.pk, )),
            obj_pk=instance.pk,
        )
    else:
        pass
    # Translate in notification receiver language
    translation.activate(instance.sender.language)
    instance.sender.create_notification(
        message=_('your friendship with %(user)s has been canceled') %
        {'user': instance.receiver},
        url=reverse('user_details', args=(instance.receiver.pk, )),
        obj_pk=instance.pk,
    )

    # Restore the language backup
    translation.activate(backup_language)


def post_save_message(sender, instance, created, **kwargs):
    # Backup of user actual language
    backup_language = translation.get_language()

    if created:

        if not instance.sender.contacts.filter(
                own=instance.sender, user=instance.receiver).exists():
            instance.sender.contacts.create(own=instance.sender,
                                            user=instance.receiver)
            instance.receiver.contacts.create(own=instance.receiver,
                                              user=instance.sender)
        else:
            result = instance.sender.contacts.filter(own=instance.sender,
                                                     user=instance.receiver)
            result.date_last_message = timezone.now()
            result = instance.receiver.contacts.filter(own=instance.receiver,
                                                       user=instance.sender)
            result.date_last_message = timezone.now()

        # Translate in notification receiver language
        translation.activate(instance.receiver.language)
        instance.receiver.create_notification(
            message=_('New message from %(user)s') % {'user': instance.sender},
            obj_pk=instance.pk,
            url=reverse('get_messages', args=(instance.sender.pk, )),
        )
    else:
        pass

    # Restore the language backup
    translation.activate(backup_language)


def pre_delete_message(sender, instance, **kwargs):
    notifications = instance.receiver.get_notification(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()


def post_save_article(sender, instance, created, **kwargs):
    # Backup of user actual language
    backup_language = translation.get_language()

    if created:
        for friend in instance.author.get_list_friends():
            # Translate in notification receiver language
            translation.activate(friend.language)
            friend.create_notification(
                message=_('%(user)s has published a new article') %
                {'user': instance.author},
                obj_pk=instance.pk,
                url=reverse('articles'),
            )
    else:
        pass

    # Restore the language backup
    translation.activate(backup_language)


def post_save_comment(sender, instance, created, **kwargs):
    # Backup of user actual language
    backup_language = translation.get_language()

    if created:
        instance.article.comments.add(instance)
        for liker in instance.article.likers.all():
            if instance.author != liker != instance.article.author:
                # Translate in notification receiver language
                translation.activate(liker.language)
                liker.create_notification(
                    message=_('%(user1)s has comments an article of '
                              '%(user2)s that you has liked') % {
                                  'user1': instance.author,
                                  'user2': instance.article.author
                              },
                    obj_pk=instance.pk,
                    url=reverse('get_comments', args=(instance.article.pk, )),
                )
            else:
                pass
        if instance.author != instance.article.author:
            # Translate in notification receiver language
            translation.activate(instance.author.language)
            instance.article.author.create_notification(
                message=_('%(user)s has comments your article') %
                {'user': instance.author},
                obj_pk=instance.pk,
                url=reverse('get_comments', args=(instance.article.pk, )),
            )
        else:
            pass
    else:
        pass

    # Restore the language backup
    translation.activate(backup_language)
