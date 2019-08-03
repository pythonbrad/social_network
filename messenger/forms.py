from django import forms
from .models import Message, User
from django.db.models import Q


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
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['date_of_birth'].widget.attrs.update({
            'class':
            'input',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class':
            'input',
        })

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'date_of_birth',
            'password',
        ]


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
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = User.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email)
        )
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
        fields = ['contains']
