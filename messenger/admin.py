from django.contrib import admin
from .models import User, Contact, Friendship, Message, Notification, Article, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Article)
admin.site.register(Comment)
