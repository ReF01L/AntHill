from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('recent/', views.recent_project, name='recent'),
    path('create/', views.create_project, name='create'),
    path('join/', views.join_project, name='join'),
    path('board/', views.board, name='board')
]
