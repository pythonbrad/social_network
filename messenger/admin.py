from django.contrib import admin
from .models import User
from .models import Contact
from .models import Friendship
from .models import Message
from .models import Notification
from .models import Article
from .models import Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Friendship)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Article)
admin.site.register(Comment)
