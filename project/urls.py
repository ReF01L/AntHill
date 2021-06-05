from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project, name='project'),
    path('command/<str:project>', views.command, name='command'),
    path('projects/', views.projects, name='projects'),
    path('create_project/', views.create_project, name='create_project'),
    path('board/', views.board, name='board'),
    path('create_issue/', views.create_issue, name='create_issue')
]
