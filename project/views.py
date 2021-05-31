from django.shortcuts import render, redirect


def project(request):
    return render(request, 'project/project.html')
