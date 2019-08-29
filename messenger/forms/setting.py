from django import forms
from django.utils.translation import gettext_lazy as _
from .utils import photo_contraint
from .account import SigninForm


class ChangeDataUserForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter the new first name'),
                'type':
                'text',
            }),
        label=_('first name').capitalize())
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                ('Enter the new last name'),
                'type':
                'text',
            }),
        label=_('last name').capitalize())
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter the new date of birth'),
                'type':
                'date',
            }),
        label=_('date of birth').capitalize())
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter your password')
            }),
        help_text='Enter your password to valid the modifications',
        label=_('password').capitalize())

    def clean_date_of_birth(self):
        return SigninForm.clean_date_of_birth(self)

    def clean_first_name(self, tag='first_name'):
        return SigninForm.clean_first_name(self, tag=tag)

    def clean_last_name(self):
        return self.clean_first_name(tag='last_name')


class ChangePhotoForm(forms.Form):
    photo = forms.ImageField()

    def clean_photo(self):
        return photo_contraint(self)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter the old password')
            }),
        label=_('old password').capitalize())
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter the new password')
            }),
        label=_('password').capitalize())
    password_verification = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class':
                'input',
                'placeholder':
                # Translators: This message is a help text
                _('Enter the new password')
            }),
        label=_('password verification').capitalize())

    def clean_password(self):
        print(dir(self))
        return SigninForm.clean_password(self)

    def clean(self):
        if 'password' not in self.cleaned_data:
            pass
        elif 'password_verification' not in self.cleaned_data:
            pass
        else:
            password = self.cleaned_data['password']
            password_verification = self.cleaned_data['password_verification']
            if password != password_verification:
                self.add_error(
                    'password_verification',
                    # Translators: This message is a error text
                    _('Password verification and'
                      ' password are different'))
