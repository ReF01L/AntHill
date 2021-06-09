from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('recent/', views.recent_project, name='recent'),
    # path('', views.project, name='project'),
    path('command/<str:project>', views.command, name='command'),
    path('projects/', views.projects, name='projects'),
    path('create_project/', views.create_project, name='create_project'),
    path('board/', views.board, name='board'),
    # path('create_issue/', views.create_issue, name='create_issue'),
    path('recent/', views.recent_project, name='recent'),
    path('create/', views.create_project, name='create'),
    path('join/', views.join_project, name='join'),
    path('board/', views.board, name='board')
]
