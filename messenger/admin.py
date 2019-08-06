from django.contrib import admin
from .models import User, Friendship, Message, Notification


admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(Notification)

# Register your models here.
