def photo_contraint(self):
    photo = self.cleaned_data['photo']
    if not type(photo) is str and photo:
        max_size = 1024 * 1024  # 1MB
        if photo.size > max_size:
            self.add_error(
                'photo', 'The photo should be lower to 1MB->1024KB,'
                ' this photo has %sMB-->%sKo' %
                (int(photo.size / 1000 / 1000), int(photo.size / 1000)))
        else:
            pass
    else:
        pass
    return photo
