from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreateForm(UserCreationForm):
    """创建用户表单"""
    class Meta:
        model = User
        fields = ('username', 'real_name', 'password1', 'password2', 'role', 'phone', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserEditForm(UserChangeForm):
    """编辑用户表单（不含密码）"""
    password = None

    class Meta:
        model = User
        fields = ('username', 'real_name', 'role', 'phone', 'email', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
