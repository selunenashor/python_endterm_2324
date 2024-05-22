import re
from datetime import datetime
import random
from pytz import timezone
from django import forms
from .models import CustomUser, PaymentMethod


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


class RenewForm(forms.Form):
    type_invoice = forms.IntegerField(widget=forms.HiddenInput())
    type_VPS = forms.CharField(widget=forms.HiddenInput())
    plan = forms.CharField(widget=forms.HiddenInput())
    CPU = forms.IntegerField(widget=forms.HiddenInput())
    RAM = forms.IntegerField(widget=forms.HiddenInput())
    SSD = forms.IntegerField(widget=forms.HiddenInput())
    OS = forms.CharField(widget=forms.HiddenInput())
    price = forms.IntegerField(widget=forms.HiddenInput())
    paymentMethod = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput())
    time = forms.IntegerField(widget=forms.NumberInput())
    totalPrice = forms.IntegerField(widget=forms.HiddenInput())
    idUser = forms.IntegerField(widget=forms.HiddenInput())
    ipVPS = forms.CharField(widget=forms.HiddenInput())

    def getInvoiceData(self):
        hanoi = timezone('Asia/Saigon')
        current_time = datetime.now(hanoi)
        current_date = current_time.strftime("%Y%m%d")
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        id = current_date + random_digits
        VPSType = self.data.get('plan')
        paymentMethod = PaymentMethod.objects.get(pk = self.data.get('paymentMethod')).name
        return {
            'id': id,
            'type': self.data.get('type_invoice'),
            'price': self.data.get('totalPrice'),
            'VPSType': VPSType,
            'status': 1,
            'paymentMethod': paymentMethod,
            'createAt': current_time,
            'finished': current_time,
            'id_user': self.data.get('idUser'),
            'targetVPS': self.data.get('ipVPS'),
            'quantity': self.data.get('quantity'),
            'time':self.data.get('time'),
            'OS': self.data.get('OS')
        }

class BaseNewVPSOrderForm(forms.Form):
    typeTemplate = forms.IntegerField(widget=forms.HiddenInput())
    type = forms.CharField(widget=forms.HiddenInput())
    OS = forms.IntegerField(widget=forms.HiddenInput())

    def getTypeTemplate(self):
        return self.data.get('typeTemplate')
    
    def getType(self):
        return self.data.get('type')
    
    def getOS(self):
        return self.data.get('OS')
    
