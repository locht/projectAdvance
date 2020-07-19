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

# class RegistrationForm(forms.Form):
class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Tên đăng nhập', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_confirm_password(self): #dãy lệnh này vẫn chạy được
        password = self.cleaned_data['Mật khẩu']
        confirm_password = self.cleaned_data['Nhập lại mật khẩu']
        if password != confirm_password:
            raise forms.ValidationError(f"Mật khẩu không trùng khớp!")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data['Tên đăng nhập']
        # if not re.search(r'^\w+$', username): 
        if not re.search(r'^[a-zA-Z0-9_.-]{4,}$', username):
            raise forms.ValidationError("Tên đăng nhập có chứa ký hiệu đặc biệt!")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại!")


    def save(self, commit=True):
        print(self.cleaned_data)
        User.objects.create_user(
            username=self.cleaned_data['username'], 
            email=self.cleaned_data['email'], 
            password=self.cleaned_data['password1']
        )

