from django import forms
from .models import Message, User, Article, Comment
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
        self.fields['date_of_birth'].help_text = "Eg: 2010-10-10"
        self.fields['date_of_birth'].widget = forms.DateInput(
            attrs={'type': 'date'})
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['photo'].help_text = "*Optionnel"
        self.fields['first_name'].help_text = "*Optionnel"
        self.fields['first_name'].widget.attrs.update({
            'class': 'input',
        })
        self.fields['last_name'].help_text = "*Optionnel"
        self.fields['last_name'].widget.attrs.update({
            'class': 'input',
        })

    password_verification = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Retape your password'
        }),
        required=True,
        help_text='Retape your password')

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
                'username is too short, min %s characters' % min_length)
        elif len(username) > max_length:
            self.add_error(
                'username',
                'username is too long, max %s characters' % max_length)
        elif " " in username:
            self.add_error('username',
                           'username should not contains the space')
        elif username[0] in '0123456789':
            self.add_error('username', 'username should not begin with a number')
        else:
            pass
        for i in string.punctuation:
            if i in username:
                self.add_error(
                    'username',
                    'username should not contains a special character')
                break
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        return email

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
                    (int(photo.size / 1000 / 1000), int(photo.size / 1000)))
            else:
                pass
        else:
            pass
        return photo

    def clean_first_name(self, tag='first_name'):
        first_name = self.cleaned_data[tag].capitalize(
        )
        max_length = 30
        if len(first_name) > max_length:
            self.add_error(
                tag, '%s is too long, max %s characters' % (tag, max_length))
        elif " " in first_name:
            self.add_error(tag, '%s should not contains the space' % tag)
        elif first_name[0] in '0123456789':
            self.add_error(tag, '%s should not begin with a number' % tag)
        else:
            pass
        return first_name

    def clean_last_name(self):
        return self.clean_first_name(tag='last_name')

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth.year >= timezone.now().year:
            self.add_error('date_of_birth', 'You are too young.')
        return date_of_birth

    def clean(self):
        password = self.cleaned_data['password']
        if "password_verification" in self.cleaned_data:
            password_verification = self.cleaned_data['password_verification']
        else:
            password_verification = ''
        if password != password_verification:
            self.add_error(
                'password_verification', 'Password verification and'
                ' password are different')


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

    username_or_email = forms.CharField(required=True)
    password = forms.CharField(required=True)

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
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
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
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
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


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            'Enter your message'
        })

    class Meta:
        model = Comment
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
