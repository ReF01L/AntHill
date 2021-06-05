from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Login', label_suffix='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'frame_3_form-field',
        }
    ))
    email = forms.CharField(label='Email', label_suffix='', widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
            'class': 'frame_3_form-field'
        }
    ))
    password = forms.CharField(label='Password', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'frame_3_form-field'
        }
    ))
    password2 = forms.CharField(label='Repeat password', label_suffix='', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repeat password',
            'class': 'frame_3_form-field'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                self.fields['email'].widget.attrs.update({
                    'class': 'frame_3_form-field-error',
                    'placeholder': 'Incorrect email',
                })
                raise forms.ValidationError('')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            self.fields['username'].widget.attrs.update({
                'class': 'frame_3_form-field-error',
                'placeholder': 'Incorrect username',
            })
            raise forms.ValidationError('')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.errors.clear()
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'frame_1_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(label='Enter your E-mail', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        self.errors.clear()
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'frame_2_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None


class NewPasswordForm(forms.Form):
    password = forms.CharField(label='Enter new password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)
        self.errors.clear()
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'reset_form-field', 'placeholder': v.label})
            v.label = ''
            v.help_text = None

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class SendCodeForm(forms.Form):
    code = forms.CharField(label='Code', label_suffix='', widget=forms.TextInput(
        attrs={
            'class': 'frame_5_form-field',
        }
    ))

    class Meta:
        model = Profile
        fields = ()

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not Profile.objects.filter(code=code).exists():
            self.fields['code'].widget.attrs.update({
                'class': 'frame_5_form-field-error',
                'placeholder': 'Incorrect code',
            })
            raise forms.ValidationError('')
        return code
