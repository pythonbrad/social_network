from django.shortcuts import reverse
from django.utils import timezone


def post_save_friendship(sender, instance, created, **kwargs):
    if created:
        instance.sender.waiting_friends.add(instance.receiver)
        instance.receiver.waiting_friends.add(instance.sender)

        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='%s said "%s"' % (instance.sender, instance.message),
            obj_pk=instance.pk,
            url=reverse('list_friendships'),
        )

    else:
        if instance.is_valided:
            instance.sender.friends.add(instance.receiver)
            instance.receiver.friends.add(instance.sender)

            instance.sender.waiting_friends.remove(instance.receiver)
            instance.receiver.waiting_friends.remove(instance.sender)

            instance.sender.notifications.create(
                receiver=instance.sender,
                message='%s has accepted your friendship' %
                (instance.receiver),
                obj_pk=instance.pk,
                url=reverse('user_details', args=(instance.receiver.pk, )),
            )

            for friend in instance.sender.friends.all():
                friend.notifications.create(
                    receiver=friend,
                    message="%s is now in friendship with %s" %
                    (instance.sender, instance.receiver),
                    obj_pk=instance.pk,
                    url=reverse('user_details', args=(instance.receiver, )))
            for friend in instance.receiver.friends.all():
                friend.notifications.create(
                    receiver=friend,
                    message="%s is now in friendship with %s" %
                    (instance.receiver, instance.sender),
                    obj_pk=instance.pk,
                    url=reverse('user_details', args=(instance.sender, )))

        else:
            pass


def pre_delete_friendship(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()

    instance.sender.waiting_friends.remove(instance.receiver)
    instance.receiver.waiting_friends.remove(instance.sender)

    instance.sender.friends.remove(instance.receiver)
    instance.receiver.friends.remove(instance.sender)

    if instance.is_valided:
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='your friendship with %s has been canceled' %
            (instance.sender),
            url=reverse('user_details', args=(instance.sender.pk, )),
            obj_pk=instance.pk,
        )
    else:
        pass
    instance.sender.notifications.create(
        receiver=instance.sender,
        message='your friendship with %s has been canceled' %
        (instance.receiver),
        url=reverse('user_details', args=(instance.receiver.pk, )),
        obj_pk=instance.pk,
    )


def post_save_message(sender, instance, created, **kwargs):
    if created:
        instance.sender.messages.add(instance)
        instance.receiver.messages.add(instance)

        if not instance.sender.contacts.filter(own=instance.sender,
                                               user=instance.receiver):
            instance.sender.contacts.create(own=instance.sender,
                                            user=instance.receiver)
            instance.receiver.contacts.create(own=instance.receiver,
                                              user=instance.sender)
        else:
            _ = instance.sender.contacts.filter(own=instance.sender,
                                                user=instance.receiver)
            _.date_last_message = timezone.now()
            _ = instance.receiver.contacts.filter(own=instance.receiver,
                                                  user=instance.sender)
            _.date_last_message = timezone.now()

        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='Message from %s' % instance.sender,
            obj_pk=instance.pk,
            url=reverse('get_messages', args=(instance.sender.pk, )),
        )
    else:
        pass


def pre_delete_message(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()


def post_save_article(sender, instance, created, **kwargs):
    if created:
        for friend in instance.author.friends.all():
            friend.notifications.create(
                receiver=friend,
                message='%s has publish a new article' % instance.author,
                obj_pk=instance.pk,
                url=reverse('articles'),
            )
    else:
        pass


def post_save_comment(sender, instance, created, **kwargs):
    if created:
        instance.article.comments.add(instance)
        for liker in instance.article.likers.all():
            if instance.author != liker != instance.article.author:
                liker.notifications.create(
                    receiver=liker,
                    message='%s has comments an article' % instance.author,
                    obj_pk=instance.pk,
                    url=reverse('get_comments', args=(instance.article.pk, )),
                )
            else:
                pass
        if instance.author != instance.article.author:
            instance.article.author.notifications.create(
                receiver=instance.article.author,
                message='%s has comments your article' % instance.author,
                obj_pk=instance.pk,
                url=reverse('get_comments', args=(instance.article.pk, )),
            )
        else:
            pass
    else:
        pass
