def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<pk>/<filename>'
    return 'user_{0}/{1}'.format(instance.get_user().pk, filename)
