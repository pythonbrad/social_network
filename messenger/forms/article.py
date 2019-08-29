from django import forms
from django.utils.translation import gettext_lazy as _
from messenger.models import Article
from messenger.models import Comment
from .utils import photo_contraint


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            # Translators: This message is a help text
            _('Enter your message')
        })

    class Meta:
        model = Article
        fields = ['contains', 'photo']

    def clean_photo(self):
        return photo_contraint(self)


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contains'].widget = forms.Textarea(
            attrs={'style': 'height: 100%'})
        self.fields['contains'].widget.attrs.update({
            'class':
            'textarea',
            'placeholder':
            # Translators: This message is a help text
            _('Enter your message')
        })

    class Meta:
        model = Comment
        fields = ['contains', 'photo']

    def clean_photo(self):
        return photo_contraint(self)
