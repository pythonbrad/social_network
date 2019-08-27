from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils import timezone
from messenger.forms import ChangePhotoForm
from messenger.forms import ChangePasswordForm
from messenger.forms import ChangeDataUserForm
from messenger.models import Article
from .utils import get_days_to_wait


def settings_view(request):
    if request.user.is_authenticated:
        datas = [{
            'title': 'My informations',
            'body': 'Modify your informations',
            'url': reverse('user_settings'),
        }, {
            'title': 'Photo of profil',
            'body': 'Change your photo of profil',
            'url': reverse('photo_settings'),
        }, {
            'title': 'Password',
            'body': 'Change your password',
            'url': reverse('password_settings'),
        }, {
            'title':
            '%s Media' % ('Enable' if request.user.no_media else 'Disable'),
            'body':
            'Click on open to Enable or Disable media to control his datas',
            'url':
            reverse('no_media_settings'),
        }]
        return render(request, 'messenger/settings.html', {
            'title': 'Settings',
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
                form.add_error('password', 'password verification error')
            else:
                date_last_update = request.user.date_updated
                days_wait = get_days_to_wait(date_last_update)
                days_to_wait = 30
                if days_wait < days_to_wait:
                    form.add_error(
                        'password',
                        'You should wait %s days to change this information'
                        ', last update: %s' %
                        (days_to_wait - days_wait, date_last_update))
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
                'title': 'User Settings',
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
                Article.objects.create(
                    author=request.user,
                    contains='Has changed his photo of profil',
                    photo=request.user.photo)
                return redirect('settings')
        else:
            form = ChangePhotoForm(initial={'photo': request.user.photo})
        return render(
            request, 'messenger/settings.html', {
                'title': 'Photo Settings',
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
                form.add_error('old_password', 'Old password error')
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
                'title': 'Password Settings',
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
