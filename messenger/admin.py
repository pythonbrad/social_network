from django.contrib import admin
from .models import Message, User, Friendship

# Register your models here.
admin.site.register(Friendship)
admin.site.register(User)
admin.site.register(Message)
