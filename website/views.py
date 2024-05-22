from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import CustomUser, VPS, Invoice

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
        return render(request, 'home.html', {'sidebar_menu': 1, 'user': CustomUser.objects.get(pk=active_username).username})
    else:
        return redirect('/login')


def order(request):
    global active_username
    if active_username is not None:
        return render(request, 'order.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_username).username})
    else:
        return redirect('/login')


def VPSList(request):
    global active_username
    if active_username is not None:
        return render(request, 'VPSList.html', {'sidebar_menu': 3, 'user': CustomUser.objects.get(pk=active_username).username, 'vpsList': VPS.objects.filter(id_user=active_username)})
    else:
        return redirect('/login')


def invoiceList(request):
    global active_username
    if active_username is not None:
        return render(request, 'invoiceList.html', {'sidebar_menu': 4, 'user': CustomUser.objects.get(pk=active_username).username, 'invoiceList': Invoice.objects.filter(id_user=active_username)})
    else:
        return redirect('/login')


def VPSDetail(request, id):
    global active_username
    if active_username is not None:
        data = VPS.objects.get(pk=id)
        return render(request, 'VPSDetail.html', {'sidebar_menu': 3, 'user': CustomUser.objects.get(pk=active_username).username, 'vps': data})
    else:
        return redirect('/login')


def invoiceDetail(request, id):
    global active_username
    if active_username is not None:
        data = Invoice.objects.get(pk=id)
        return render(request, 'invoiceDetail.html', {'sidebar_menu': 4, 'user': CustomUser.objects.get(pk=active_username).username, 'invoice': data})
    else:
        return redirect('/login')


def invoiceConfirm(request):
    global active_username
    if active_username is not None:
        return render(request, 'invoiceConfirm.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_username).username})
    else:
        return redirect('/login')


def create_user(username, password, email, phone):
    new_user = CustomUser()
    new_user.username = username
    new_user.password = password
    new_user.email = email
    new_user.phone = phone
    new_user.save()
