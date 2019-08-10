from django import forms
from .models import Message, User, Article
from django.db.models import Q
from django.utils import timezone
import string


class SigninForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Enter your email'
        })
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date'})
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'input',
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'password', 'photo']

    def clean_username(self):
        username = self.cleaned_data['username']
        min_length = 4
        max_length = 30
        if len(username) < min_length:
            self.add_error(
                'username',
                'username is too short, min %s characters' % min_length)
        elif len(username) > max_length:
            self.add_error(
                'username',
                'username is too long, max %s characters' % max_length)
        elif " " in username:
            self.add_error('username',
                           'username should not contains the space')
        else:
            pass
        for i in string.punctuation:
            if i in username:
                self.add_error(
                    'username',
                    'username should not contains a special character')
                break
        return username.lower()

    def clean_password(self):
        password = self.cleaned_data['password']
        min_length = 4
        if len(password) < min_length:
            self.add_error(
                'password',
                'password is too short, min %s characters' % min_length)
        else:
            pass
        return password

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if not type(photo) is str:
            max_size = 1024 * 1024  # 1MB
            if photo.size > max_size:
                self.add_error(
                    'photo', 'The photo should be lower to 1MB->1024KB,'
                    ' this photo has %sMB-->%sKo' %
                    (photo.size / 1000 / 1000, photo.size / 1000))
            else:
                pass
        else:
            pass
        return photo

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth.year >= timezone.now().year:
            self.add_error('date_of_birth', 'You are too young.')
        return date_of_birth


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username_or_email'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Type your Username or Email'
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class':
            'input',
            'placeholder':
            'Type your Password'
        })

    username_or_email = forms.CharField()
    password = forms.CharField()

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email'].lower()
        password = self.cleaned_data['password']
        user = User.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email))
        if user:
            user = user.filter(password=password)
            if user:
                self.user = user[0]
            else:
                self.add_error('password', 'password invalid')
        else:
            self.add_error('username_or_email', 'username|email invalid')

    def get_user(self):
        return self.user


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea()
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Message
        fields = ['contains', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            max_size = 1024 * 1024  # 1MB
            if photo.size > max_size:
                self.add_error(
                    'photo', 'The photo should be lower to 1MB->1024KB,'
                    ' this photo has %sMB-->%sKo' %
                    (photo.size / 1000 / 1000, photo.size / 1000))
            else:
                pass
        else:
            pass
        return photo


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea()
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Article
        fields = ['contains', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            max_size = 1024 * 1024  # 1MB
            if photo.size > max_size:
                self.add_error(
                    'photo', 'The photo should be lower to 1MB->1024KB,'
                    ' this photo has %sMB-->%sKo' %
                    (photo.size / 1000 / 1000, photo.size / 1000))
            else:
                pass
        else:
            pass
        return photo
