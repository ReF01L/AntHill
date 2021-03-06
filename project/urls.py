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
    path('<slug:slug>/create_sprint/', views.create_sprint, name='create_sprint'),
    path('<slug:slug>/edit_sprint/', views.edit_sprint, name='edit_sprint'),
    path('<slug:slug>/delete_sprint/', views.delete_sprint, name='delete_sprint'),
    path('<slug:project_slug>/issue/<slug:issue_slug>/', views.issue, name='issue'),
    path('<slug:project_slug>/delete_issue/<slug:issue_slug>/', views.delete_issue, name='delete_issue'),
]
