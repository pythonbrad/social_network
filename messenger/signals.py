def post_create_friendship(sender, instance, created, **kwargs):
    if created:
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='%s said "%s"' % (instance.sender, instance.message),
            obj_pk=instance.pk,
        )
    else:
        if instance.is_valided:
            instance.sender.notifications.create(
                receiver=instance.sender,
                message='%s has accepted your friendship' % (instance.receiver),
                obj_pk=instance.pk,
            )
        else:
            pass


def post_delete_friendship(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()


def post_create_message(sender, instance, created, **kwargs):
    if created:
        instance.receiver.notifications.create(
            receiver=instance.receiver,
            message='Message from %s' % instance.sender,
            obj_pk=instance.pk,
        )
    else:
        pass


def post_delete_message(sender, instance, **kwargs):
    notifications = instance.receiver.notifications.filter(obj_pk=instance.pk)
    for notification in notifications:
        notification.delete()
