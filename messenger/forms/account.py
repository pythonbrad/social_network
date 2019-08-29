from .utils import photo_contraint
from messenger.models import User
from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import string


class SigninForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            # Translators: This message is a help text
            _('Enter your username')
        })
        self.fields['email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            # Translators: This message is a help text
            _('Enter your email')
        })
        # Translators: This message is a help text
        self.fields['date_of_birth'].help_text = _("Eg: %(date)s") % {
            'date': '2010-10-10'
        }
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date'})
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'input',
        })
        # Translators: This message is a help text
        self.fields['photo'].help_text = _("*Optional")
        # Translators: This message is a help text
        self.fields['first_name'].help_text = _("*Optional")
        self.fields['first_name'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['last_name'].help_text = _("*Optional")
        self.fields['last_name'].widget.attrs.update({
            'class': 'input',
        })

    password_verification = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                # Translators: This message is a help text
                'placeholder': _('Retype your password')
            }),
        required=True,
        # Translators: This message is a help text
        help_text=_('Retype your password'),
        label=_('password verification').capitalize())

    class Meta:
        model = User
        fields = [
            'username', 'email', 'date_of_birth', 'password', 'photo',
            'first_name', 'last_name'
        ]

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        min_length = 4
        max_length = 30
        if len(username) < min_length:
            self.add_error(
                'username',
                # Translators: This message is a error text
                _('username is too short, min %(min_length)d characters') %
                {'min_length': min_length})
        elif User.objects.filter(username=username).exists():
            # Translators: This message is a error text
            self.add_error('username', _('This username is already used'))
        elif len(username) < min_length:
            self.add_error(
                'username',
                # Translators: This message is a error text
                _('username is too short, min %(min_length)d characters') %
                {'min_length': min_length})
        elif len(username) > max_length:
            self.add_error(
                'username',
                # Translators: This message is a error text
                _('username is too long, max %(max_length)d characters') %
                {'max_length': max_length})
        elif " " in username:
            self.add_error(
                'username',
                # Translators: This message is a error text
                _('username should not contains the space'))
        elif username[0] in '0123456789':
            self.add_error(
                'username',
                # Translators: This message is a error text
                _('username should not begin with a number'))
        else:
            pass
        for i in string.punctuation:
            if i in username:
                self.add_error(
                    'username',
                    # Translators: This message is a error text
                    _('username should not contains a special character'))
                break
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                # Translators: This message is a error text
                _('This email is already used'))
        else:
            pass
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        min_length = 4
        if len(password) < min_length:
            self.add_error(
                'password',
                # Translators: This message is a error text
                _('password is too short, min %(min_length)d characters') %
                {'min_length': min_length})
        else:
            pass
        return password

    def clean_photo(self):
        return photo_contraint(self)

    def clean_first_name(self, tag='first_name'):
        first_name = self.cleaned_data[tag]
        max_length = 30
        if first_name:
            if len(first_name) > max_length:
                self.add_error(
                    tag,
                    # Translators: This message is a error text
                    _('%(tag)s is too long, max %(max_length)d characters') % {
                        'tag': tag,
                        'max_length': max_length
                    })
            elif " " in first_name:
                self.add_error(
                    tag,
                    # Translators: This message is a error text
                    _('%(tag)s should not contains the space') % {'tag': tag})
            elif first_name[0] in '0123456789':
                self.add_error(
                    tag,
                    # Translators: This message is a error text
                    _('%(tag)s should not begin with a number') % {'tag': tag})
            else:
                pass
        else:
            pass
        return first_name

    def clean_last_name(self):
        return self.clean_first_name(tag='last_name')

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth.year >= timezone.now().year:
            self.add_error(
                'date_of_birth',
                # Translators: This message is a error text
                _('You are too young.'))
        return date_of_birth

    def clean(self):
        if 'password' not in self.cleaned_data:
            pass
        elif "password_verification" not in self.cleaned_data:
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
            else:
                pass


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username_or_email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            # Translators: This message is a help text
            _('Type your Username or Email')
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            # Translators: This message is a help text
            _('Type your Password')
        })

    username_or_email = forms.CharField(required=True,
                                        label=_('Username or Email'))
    password = forms.CharField(required=True, label=_('password'))

    def clean(self):
        if 'username_or_email' not in self.cleaned_data:
            pass
        elif 'password' not in self.cleaned_data:
            pass
        else:
            username_or_email = self.cleaned_data['username_or_email'].lower()
            password = self.cleaned_data['password']
            user = User.objects.filter(
                Q(username=username_or_email) | Q(email=username_or_email))
            if user.exists():
                user = user.filter(password=password)
                if user.exists():
                    self.user = user[0]
                else:
                    self.add_error(
                        'password',
                        # Translators: This message is a error text
                        _('password invalid'))
            else:
                self.add_error(
                    'username_or_email',
                    # Translators: This message is a error text
                    _('username or email invalid'))

    def get_user(self):
        return self.user
