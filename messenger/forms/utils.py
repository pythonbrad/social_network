from django.utils.translation import gettext_lazy as _


def photo_contraint(self):
    photo = self.cleaned_data['photo']
    if not type(photo) is str and photo:
        max_size = 1024 * 1024  # 1MB
        if photo.size > max_size:
            self.add_error(
                'photo',
                # Translators: This message is a error text
                _('The photo should be lower to 1MB or 1024KB,'
                  ' this photo has %(size_in_mb)dMB or %(size_in_kb)dKb') % {
                      'size_in_mb': int(photo.size / 1000 / 1000),
                      'size_in_kb': int(photo.size / 1000)
                  })
        else:
            pass
    else:
        pass
    return photo
