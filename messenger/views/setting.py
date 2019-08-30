from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils import timezone
from django.utils import translation
from django.utils.translation import gettext as _
from messenger.forms import ChangePhotoForm
from messenger.forms import ChangePasswordForm
from messenger.forms import ChangeDataUserForm
from messenger.models import Article
from .utils import get_days_to_wait


def settings_view(request):
    if request.user.is_authenticated:
        datas = [
            {
                'title': _('My informations'),
                'body': _('Modify your informations'),
                'url': reverse('user_settings'),
            },
            {
                'title': _('Photo of profil'),
                'body': _('Change your photo of profil'),
                'url': reverse('photo_settings'),
            },
            {
                'title': _('Password'),
                'body': _('Change your password'),
                'url': reverse('password_settings'),
            },
            {
                'title':
                '%s Media' %
                (_('Enable') if request.user.no_media else _('Disable')),
                'body':
                _('Click on open to Enable or Disable media to control his datas'
                  ),
                'url':
                reverse('no_media_settings'),
            },
            {
                'title': 'English Language',
                'body': 'Click on %s to set English Language' % _('Open'),
                'url': reverse('set_language', args=('en', )),
            },
            {
                'title':
                'Langue Francaise',
                'body':
                'Click sur %s pour passer a la language Francaise' % _('Open'),
                'url':
                reverse('set_language', args=('fr', )),
            },
        ]
        return render(request, 'messenger/settings.html', {
            'title': _('Settings'),
            'datas': datas,
        })
    else:
        return redirect('login')


def user_settings_view(request):
    if request.user.is_authenticated:
        if request.POST:
            form = ChangeDataUserForm(request.POST, request.FILES)
            password_entry = request.POST.get('password', None)
            if password_entry != request.user.password:
                form.add_error(
                    'password',
                    # Translators: This message is a error text
                    _('password verification error'))
            else:
                date_last_update = request.user.date_updated
                days_wait = get_days_to_wait(date_last_update)
                days_to_wait = 30
                if days_wait < days_to_wait:
                    form.add_error(
                        'password',
                        # Translators: This message is a error text
                        _('You should wait %(days_to_wait)d days to change'
                          ' this information, last update: %(days_wait)s') % {
                              'days_to_wait': (days_to_wait - days_wait),
                              'date_last_update': date_last_update
                          })
                else:
                    pass
            if form.is_valid():
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.date_of_birth = form.cleaned_data['date_of_birth']
                request.user.date_updated = timezone.now()
                request.user.save()
                return redirect('settings')
            else:
                pass
        else:
            form = ChangeDataUserForm({
                'date_of_birth': request.user.date_of_birth,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            })
        return render(
            request, 'messenger/settings.html', {
                'title': _('User Settings'),
                'form': form,
                'settings_url': reverse('user_settings'),
            })
    else:
        return redirect('login')


def photo_settings_view(request):
    if request.user.is_authenticated:
        if request.POST:
            form = ChangePhotoForm(request.POST, request.FILES)
            if form.is_valid():
                request.user.photo = form.cleaned_data['photo']
                request.user.save()
                Article.make_notification(
                    author=request.user,
                    contains=_('Has changed his photo of profil'),
                    photo=request.user.photo)
                return redirect('settings')
        else:
            form = ChangePhotoForm(initial={'photo': request.user.photo})
        return render(
            request, 'messenger/settings.html', {
                'title': _('Photo Settings'),
                'form': form,
                'settings_url': reverse('photo_settings'),
            })
    else:
        return redirect('login')


def password_settings_view(request):
    if request.user.is_authenticated:
        if request.POST:
            form = ChangePasswordForm(request.POST, request.FILES)
            old_password = request.POST.get('old_password', None)
            if old_password != request.user.password:
                form.add_error(
                    'old_password',
                    # Translators: This message is a error text
                    _('Old password error'))
            else:
                pass
            if form.is_valid():
                request.user.password = form.cleaned_data['password']
                request.user.save()
                return redirect('settings')
        else:
            form = ChangePasswordForm()
        return render(
            request, 'messenger/settings.html', {
                'title': _('Password Settings'),
                'form': form,
                'settings_url': reverse('password_settings'),
            })
    else:
        return redirect('login')


def no_media_settings_view(request):
    if request.user.is_authenticated:
        request.user.no_media = False if request.user.no_media else True
        request.user.save()
        return redirect('settings')
    else:
        return redirect('login')


def set_language(request, lang):
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    if request.user.is_authenticated:
        request.user.language = lang
        request.user.save()
        return redirect('settings')
    else:
        return redirect('home')
