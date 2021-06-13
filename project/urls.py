from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'project'

urlpatterns = [
    path('', RedirectView.as_view(url='projects'), name='_projects'),
    path('projects/', views.projects, name='projects'),
    path('recent/', views.recent_project, name='recent'),
    path('create/', views.create_project, name='create'),
    path('join/', views.join_project, name='join'),
    path('<str:project_key>/', RedirectView.as_view(url='board'), name='_board'),
    path('<slug:slug>/board/', views.board, name='board'),
    path('<slug:slug>/issues/', views.issues, name='issues'),
    path('<slug:slug>/log/', views.log, name='log'),
    path('<slug:slug>/create/', views.create_issue, name='create_issue'),
    path('<slug:project_slug>/issue/<slug:issue_slug>/', views.issue, name='issue'),
]
