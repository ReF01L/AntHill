from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from AntHill import settings
from .forms import UserRegistrationForm, LoginForm, UserEditForm, ProfileEditForm, ForgotPasswordForm, NewPasswordForm
from .models import Profile


def new_password(request, uidb64, token):
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            user_id = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'account/success_password.html')
    return render(request, 'account/new_password.html', {
        'form': NewPasswordForm()
    })


@require_GET
def profile(request):
    user = Profile.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'user': user})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
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
    page = int(request.POST.get('page') or request.GET.get('page') or 0)
    errors = {
        'login': '',
        'reset': ''
    }
    if page == 1:
        form = LoginForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('account:profile')
            errors['login'] = 'The username or password you entered is incorrect'
        return render(request, 'account/login.html', {
            'form': form,
            'page': page,
            'errors': errors
        })
    if page == 2:
        form = ForgotPasswordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    user = User.objects.get(email=cd['email'])
                    if user is not None and user.is_active:
                        theme = 'RESET PASSWORD AntHill'
                        data = {
                            'email': user.email,
                            'domain': '127.0.0.1:8000',
                            'site_name': 'AntHill',
                            'uid': urlsafe_base64_encode(force_bytes(user.id)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http'
                        }

                        email = EmailMessage(theme, render_to_string('account/password_reset_message.html', data),
                                             settings.EMAIL_HOST_USER, [user.email])
                        email.send()

                        return render(request, 'account/login.html', {
                            'page': 4,
                        })
                except User.DoesNotExist:
                    pass
            errors['reset'] = 'User with this email is not registered'
        return render(request, 'account/login.html', {
            'form': form,
            'page': page,
            'errors': errors
        })
    return render(request, 'account/login.html')


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('account:user_login')
    return render(request, 'account/register.html', {
        'form': form,
        'page': 3
    })
