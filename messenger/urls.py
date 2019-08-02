from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signin', views.signin_view, name='signin'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('panel', views.panel_view, name='panel'),
    path('friendships', views.get_list_friendship_view,
         name='list_friendships'),
    path('friendships/create/<int:pk>',
         views.create_friendship_view,
         name='create_friendship'),
    path('friendships/accept/<int:pk>',
         views.accept_friendship_view,
         name='accept_friendship'),
    path('friendships/delete/<int:pk>',
         views.delete_friendship_view,
         name='delete_friendship'),
    path('users', views.get_list_users_view, name='list_users'),
    path('friends', views.get_list_friends_view, name='list_friends'),
    path('friends/delete/<int:pk>', views.delete_friend_view, name='delete_friend'),
]
