from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='profile'),
    path('success_reset_password/', views.success_reset_password, name='success_reset_password')
]
