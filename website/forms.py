import re
from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'login_account', 'placeholder': 'Tài khoản'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'login_password', 'placeholder': 'Mật khẩu'}))

    def username_exists(self, username, password):
        return CustomUser.objects.filter(username=username, password=password).exists()

    def check(self):
        username = self.data['username']
        password = self.data['password']

        return self.username_exists(username=username, password=password)

    def getID(self):
        username = self.data['username']
        password = self.data['password']
        return CustomUser.objects.get(username=username, password=password).id


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'register_account_input', 'placeholder': 'Tài khoản'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'register_password_input', 'placeholder': 'Mật khẩu'}))
    passwordConfirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'register_password_input_repeat', 'placeholder': 'Mật khẩu'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'id': 'register_email_input', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'register_phone_input', 'placeholder': 'Số điện thoại'}))

    def username_exists(self, username):
        return CustomUser.objects.filter(username=username).exists()

    def check(self):
        return self.getData()['code']

    def getData(self):
        username = self.data['username']
        password = self.data['password']
        passwordConfirm = self.data.get('passwordConfirm')
        email = self.data['email']
        phone = self.data['phone']
        if len(username) < 6 or len(username) > 20 or (not username.isalnum()) or (' ' in username) or username[0].isdigit():
            return {
                'code': 1
            }

        if len(password) < 6 or len(password) > 20:
            return {
                'code': 2
            }
        if password and passwordConfirm and password != passwordConfirm:
            return {
                'code': 3
            }
        if not re.match(r'^0[0-9]{9}$', phone):
            return {
                'code': 4
            }
        if self.username_exists(username):
            return {
                'code': 5
            }
        return {
            'code': 0,
            'data': {
                'username': username,
                'password': password,
                'phone': phone,
                'email': email
            }

        }
