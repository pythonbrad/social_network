def post_save_friendship(sender, instance, created, **kwargs):
    if created:
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='%s said "%s"' % (instance.sender, instance.message),
            obj_pk=instance.pk,
        )

        instance.sender.waiting_friends.add(instance.receiver)
        instance.receiver.waiting_friends.add(instance.sender)

    else:
        if instance.is_valided:
            instance.sender.notifications.create(
                receiver=instance.sender,
                message='%s has accepted your friendship' %
                (instance.receiver),
                obj_pk=instance.pk,
            )

            instance.sender.friends.add(instance.receiver)
            instance.receiver.friends.add(instance.sender)

            instance.sender.waiting_friends.remove(instance.receiver)
            instance.receiver.waiting_friends.remove(instance.sender)

        else:
            pass


def post_delete_friendship(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()

    instance.sender.waiting_friends.remove(instance.receiver)
    instance.receiver.waiting_friends.remove(instance.sender)

    instance.sender.friends.remove(instance.receiver)
    instance.receiver.friends.remove(instance.sender)

    if instance.is_valided:
        instance.sender.notifications.create(
            receiver=instance.sender,
            message='your friendship with %s has been canceled' %
            (instance.receiver),
            obj_pk=instance.pk,
        )
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='your friendship with %s has been canceled' %
            (instance.sender),
            obj_pk=instance.pk,
        )
    else:
        instance.sender.notifications.create(
            receiver=instance.sender,
            message='your friendship with %s has been refused' %
            (instance.receiver),
            obj_pk=instance.pk,
        )


def post_save_message(sender, instance, created, **kwargs):
    if created:
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='Message from %s' % instance.sender,
            obj_pk=instance.pk,
        )
        instance.sender.messages.add(instance)
        instance.receiver.messages.add(instance)
    else:
        pass


def post_delete_message(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()