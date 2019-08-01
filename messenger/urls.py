from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signin', views.signin_view, name='signin'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('panel', views.panel_view, name='panel'),
    path('panel/<int:user_pk>', views.panel_view, name='panel'),
]
