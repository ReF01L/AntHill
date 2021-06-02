from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .forms import UserRegistrationForm, LoginForm, UserEditForm, ProfileEditForm, NewPasswordForm
from .models import Profile


@require_GET
def profile(request):
    if not request.user.is_anonymous:
        user = Profile.objects.get(user=request.user)
        return render(request, 'account/profile.html', {'user': user})
    return home(request, False)


def home(request, error):
    if not request.user.is_anonymous:
        return profile(request)
    if request.path == '/account/login/':
        return render(request, 'account/login.html', {
            'form': LoginForm(),
            'error': error
        })
    elif request.path == '/account/register/':
        return render(request, 'account/register.html', {
            'form': UserRegistrationForm(),
            'error': error
        })
    return redirect('account:user_login')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def user_logout(request):
    logout(request)
    return redirect('account:user_login')


@csrf_exempt
def user_login(request):
    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect('account:profile')
        error = True
    return home(request, error)


def register(request):
    error = False
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('account:user_login')
        error = True
    return home(request, error)


def success_reset_password(request):
    return render(request, 'account/success_reset_password.html', {
        'form': NewPasswordForm()
    })
