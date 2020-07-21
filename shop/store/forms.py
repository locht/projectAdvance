from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re

class EditProfileForm(UserChangeForm):
    # username = forms.CharField(help_text=False)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

class RegistrationForm(forms.Form):
# class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Tên đăng nhập', max_length=30, widget=forms.TextInput(attrs={'class':"form-control"}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':"form-control"}))
    # password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    # password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())

    # first_name = forms.CharField(label='Tên', widget=forms.TextInput(attrs={'class':"form-control"}))
    # last_name = forms.CharField(label='Họ', widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    confirm_password = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput(attrs={'class':"form-control"}))

    # class Meta:
    #     model = User
    #     fields = (
    #         'username',
    #         'email',
    #         'password',
    #         'confirm_password',
    #         # 'password1',
    #         # 'password2',

    #     )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username): 
            raise forms.ValidationError("Tên đăng nhập có chứa ký hiệu đặc biệt!")
        elif not re.search(r'^[a-zA-Z0-9_.-]{4,}$', username):
            raise forms.ValidationError("Tên đăng nhập phải có ít nhất 4 kí tự!")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(f"Tài khoản '{username}' đã tồn tại!")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email '{email}' đã tồn tại!")

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(f"Mật khẩu không trùng khớp!")
        return confirm_password


    def save(self, commit=True):
        print(self.cleaned_data)
        User.objects.create_user(
            username=self.cleaned_data['username'], 
            email=self.cleaned_data['email'], 
            password=self.cleaned_data['password1']
        )

class LoginForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập', max_length=30, widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class':"form-control"}))
