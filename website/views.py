from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import CustomUser

active_username = None


def login(request):
    global active_username
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.check():
            active_username = form.getID()
            return redirect('/home')
        else:
            return render(request, 'login.html', {'form': LoginForm(), 'err_message': "Tài khoản hoặc mật khẩu không chính xác"})
    else:
        return render(request, 'login.html', {'form': LoginForm()})


def logout(request):
    global active_username
    active_username = None
    return redirect('/login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.check() == 0:
            data = form.getData()['data']
            create_user(data['username'], data['password'],
                        data['email'], data['phone'])
            return redirect('/login')
        else:

            return render(request, 'register.html', {
                'form': form, 'err_code': form.check()})
    else:
        return render(request, 'register.html', {'form': RegisterForm()})


def home(request):
    global active_username
    if active_username is not None:
        return render(request, 'home.html', {'sidebar_menu': 1})
    else:
        return redirect('/login')


def order(request):
    global active_username
    if active_username is not None:
        return render(request, 'order.html', {'sidebar_menu': 2})
    else:
        return redirect('/login')


def VPSList(request):
    global active_username
    if active_username is not None:
        return render(request, 'VPSList.html', {'sidebar_menu': 3})
    else:
        return redirect('/login')


def invoiceList(request):
    global active_username
    if active_username is not None:
        return render(request, 'invoiceList.html', {'sidebar_menu': 4})
    else:
        return redirect('/login')


def VPSDetail(request):
    global active_username
    if active_username is not None:
        return render(request, 'VPSDetail.html', {'sidebar_menu': 3})
    else:
        return redirect('/login')


def invoiceDetail(request):
    global active_username
    if active_username is not None:
        return render(request, 'invoiceDetail.html', {'sidebar_menu': 4})
    else:
        return redirect('/login')


def invoiceConfirm(request):
    return render(request, 'invoiceConfirm.html')


def create_user(username, password, email, phone):
    new_user = CustomUser(
        username=username, password=password, email=email, phone=phone)
    new_user.save()
