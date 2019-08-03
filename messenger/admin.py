from django.contrib import admin
from .models import User, Friendship, Message, Notification

'''

la desinsciption se fait par etape del message, notification, ..., after user


'''


admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(Notification)

# Register your models here.
