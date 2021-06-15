from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'account'

urlpatterns = [
    path('', RedirectView.as_view(url='/account/login/'), name='goto_login'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('new_password/<str:uidb64>/<str:token>/', views.new_password, name='new_password'),
]
