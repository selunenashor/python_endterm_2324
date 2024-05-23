from datetime import datetime
import random
from pytz import timezone
from dateutil.relativedelta import relativedelta
import string
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, RenewForm, BaseNewVPSOrderForm
from .models import CustomUser, VPS, Invoice, PaymentMethod, VPSTypeTemplate, VPSTemplate, OSTemplate

active_user = None


class InvoiceTemp:
    def __init__(self, type_invoice, type_VPS, plan, CPU, RAM, SSD, OS, price, list_payment, id_user, ip_VPS=None) -> None:
        self.type_invoice = type_invoice
        self.type_VPS = type_VPS
        self.plan = plan
        self.CPU = CPU
        self.RAM = RAM
        self.SSD = SSD
        self.OS = OS.id
        self.price = price
        self.list_payment = list_payment
        self.id_user = id_user
        self.ip_VPS = ip_VPS


def login(request):
    global active_user
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.check():
            active_user = form.getID()
            return redirect('/home')
        else:
            return render(request, 'login.html', {'form': LoginForm(), 'err_message': "Tài khoản hoặc mật khẩu không chính xác"})
    else:
        return render(request, 'login.html', {'form': LoginForm()})


def logout(request):
    global active_user
    active_user = None
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
    global active_user
    if active_user is not None:
        total_vps = VPS.objects.filter(id_user=active_user).count()
        total_running = VPS.objects.filter(
            id_user=active_user, status=1).count()
        total_invoice = Invoice.objects.filter(id_user=active_user).count()
        total_invoice_pending = Invoice.objects.filter(
            id_user=active_user, status=1).count()
        return render(request, 'home.html', {'sidebar_menu': 1, 'user': CustomUser.objects.get(pk=active_user).username, 'data': {
            "total_vps": total_vps,
            "total_running": total_running,
            "total_invoice": total_invoice,
            "total_invoice_pending": total_invoice_pending,
        }})
    else:
        return redirect('/login')


def orderStep1(request):
    global active_user
    if active_user is not None:
        vpsTypeTemp = VPSTypeTemplate.objects.all()
        form = BaseNewVPSOrderForm()
        return render(request, 'order.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_user).username, 'vpsTypeTemp': vpsTypeTemp, 'form': form})
    else:
        return redirect('/login')


def orderStep2(request):
    global active_user
    if active_user is not None:
        form = BaseNewVPSOrderForm(request.POST)
        vpsType = VPSTemplate.objects.filter(type_id=form.getTypeTemplate())
        return render(request, 'order.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_user).username, 'vpsType': vpsType, 'form': form})
    else:
        return redirect('/login')


def orderStep3(request):
    global active_user
    if active_user is not None:
        form = BaseNewVPSOrderForm(request.POST)
        OS = OSTemplate.objects.all()
        return render(request, 'order.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_user).username, 'os': OS, 'form': form})
    else:
        return redirect('/login')


def orderConfirm(request):
    global active_user
    if active_user is not None:
        form = BaseNewVPSOrderForm(request.POST)
        plan = VPSTemplate.objects.get(pk=form.getType())
        paymentMethods = PaymentMethod.objects.all()
        data = InvoiceTemp(1, VPSTypeTemplate.objects.get(pk=form.getTypeTemplate()).name, plan.id, plan.CPU, plan.RAM,
                           plan.SSD, OSTemplate.objects.get(pk=form.getOS()), plan.pricePerMonth, paymentMethods, active_user)
        initial_data = {
            'type_invoice': data.type_invoice,
            'type_VPS': data.type_VPS,
            'plan': data.plan,
            'CPU': data.CPU,
            'RAM': data.RAM,
            'SSD': data.SSD,
            'OS': data.OS,
            'price': data.price,
            'quantity': 1,
            'time': 1,
            'paymentMethod': data.list_payment[0].id,
            'totalPrice': data.price,
            'idUser': data.id_user,
            'ipVPS': data.ip_VPS
        }
        form = RenewForm(initial=initial_data)
        return render(request, 'invoiceConfirm.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_user).username, 'data': data, 'form': form})
    else:
        return redirect('/login')


def VPSList(request):
    global active_user
    if active_user is not None:
        return render(request, 'VPSList.html', {'sidebar_menu': 3, 'user': CustomUser.objects.get(pk=active_user).username, 'vpsList': VPS.objects.filter(id_user=active_user)})
    else:
        return redirect('/login')


def invoiceList(request):
    global active_user
    if active_user is not None:
        return render(request, 'invoiceList.html', {'sidebar_menu': 4, 'user': CustomUser.objects.get(pk=active_user).username, 'invoiceList': Invoice.objects.filter(id_user=active_user)})
    else:
        return redirect('/login')


def VPSDetail(request, id):
    global active_user
    if active_user is not None:
        data = VPS.objects.get(pk=id)
        return render(request, 'VPSDetail.html', {'sidebar_menu': 3, 'user': CustomUser.objects.get(pk=active_user).username, 'vps': data})
    else:
        return redirect('/login')


def invoiceDetail(request, id):
    global active_user
    if active_user is not None:
        data = Invoice.objects.get(pk=id)
        return render(request, 'invoiceDetail.html', {'sidebar_menu': 4, 'user': CustomUser.objects.get(pk=active_user).username, 'invoice': data})
    else:
        return redirect('/login')


def createVPS(request, id):
    global active_user
    if active_user is not None:
        invoice = Invoice.objects.get(pk=id)
        type = VPSTemplate.objects.get(pk=invoice.VPSType).type.id
        for i in range(invoice.quantity):
            new_ip = createIP(type)
            while not checkIP(new_ip):
                new_ip = createIP(type)
            VPSTemp = VPSTemplate.objects.get(pk=invoice.VPSType)
            hanoi = timezone('Asia/Saigon')
            expired_date = datetime.now(hanoi) + relativedelta(months=invoice.time)
            create_vps(new_ip, VPSTemp.type.id, VPSTemp.id, VPSTemp.CPU, VPSTemp.RAM, VPSTemp.SSD,
                       VPSTemp.pricePerMonth, expired_date, createUsername(), createPassword(), invoice.OS)
        invoice.status = 2
        invoice.save()
        return redirect('/VPSList')
    else:
        return redirect('/login')
    
def renewVPS(request, id):
    global active_user
    if active_user is not None:
        invoice = Invoice.objects.get(pk=id)
        vps = VPS.objects.get(ip=invoice.targetVPS)
        vps.expired_date+=relativedelta(months=invoice.time)
        vps.save()
        invoice.status = 2
        invoice.save()
        return redirect('/VPSDetail/' + str(vps.id))
    else:
        return redirect('/login')

def changeVPSStatus(request, id):
    vps = VPS.objects.get(pk=id)
    if (vps.status == 1):
        vps.status = 2
    else:
        vps.status = 1
    vps.save()
    return redirect('/VPSDetail/' + str(id))


def renewVPSConfirm(request, id):
    global active_user
    if active_user is not None:
        vps = VPS.objects.get(pk=id)
        paymentMethods = PaymentMethod.objects.all()
        data = InvoiceTemp(2, vps.type, vps.plan, vps.CPU, vps.RAM, vps.SSD, vps.OS,
                           vps.price, paymentMethods, active_user, vps.ip)
        initial_data = {
            'type_invoice': data.type_invoice,
            'type_VPS': data.type_VPS,
            'plan': data.plan,
            'CPU': data.CPU,
            'RAM': data.RAM,
            'SSD': data.SSD,
            'OS': data.OS,
            'price': data.price,
            'quantity': 1,
            'time': 1,
            'paymentMethod': data.list_payment[0].id,
            'totalPrice': data.price,
            'idUser': data.id_user,
            'ipVPS': data.ip_VPS
        }
        form = RenewForm(initial=initial_data)
        return render(request, 'invoiceConfirm.html', {'sidebar_menu': 2, 'user': CustomUser.objects.get(pk=active_user).username, 'data': data, 'form': form})
    else:
        return redirect('/login')


def invoice_renewVPS(request):
    global active_user
    if active_user is not None:
        form = RenewForm(data=request.POST)
        invoice = form.getInvoiceData()
        quantity = 1
        if(invoice['quantity']): quantity = invoice['quantity']
        create_invoice(invoice['id'], invoice['id_user'], invoice['type'], invoice['price'],
                       invoice['VPSType'], invoice['paymentMethod'], invoice['createAt'], invoice['finished'], quantity , invoice['time'], invoice['OS'], invoice['targetVPS'])
        data = Invoice.objects.get(pk=invoice['id'])
        return redirect('/invoiceDetail/' + str(data.id))
    else:
        return redirect('/login')

def cancelPayment(request, id):
    global active_user
    if active_user is not None:
        invoice = Invoice.objects.get(pk=id)
        invoice.status = 0
        invoice.save()
        return redirect('/invoiceDetail/' + id)
    else: 
        return redirect('/login')

def deleteVPS(request, id):
    vps = VPS.objects.get(pk=id)
    vps.delete()
    return redirect('/VPSList')


def create_vps(ip, type, plan, cpu, ram, ssd, price, expried_date, username, password, OS_id):
    new_VPS = VPS()
    new_VPS.ip = ip
    new_VPS.id_user = CustomUser.objects.get(pk=active_user)
    new_VPS.type = type
    new_VPS.plan = plan
    new_VPS.CPU = cpu
    new_VPS.RAM = ram
    new_VPS.SSD = ssd
    new_VPS.price = price
    new_VPS.expired_date = expried_date
    new_VPS.username = username
    new_VPS.password = password
    new_VPS.status = 1
    new_VPS.OS = OSTemplate.objects.get(pk=OS_id)
    new_VPS.save()


def create_user(username, password, email, phone):
    new_user = CustomUser()
    new_user.username = username
    new_user.password = password
    new_user.email = email
    new_user.phone = phone
    new_user.save()


def create_invoice(id, id_user, type, price, VPSType, paymentMethod, createAt, finished, quantity, time, OS, targetVPS=None):
    new_invoice = Invoice()
    new_invoice.id = id
    new_invoice.id_user = CustomUser.objects.get(pk=id_user)
    new_invoice.type = type
    new_invoice.price = price
    new_invoice.VPSType = VPSType
    new_invoice.status = 1
    new_invoice.paymentMethod = paymentMethod
    new_invoice.createAt = createAt
    new_invoice.finished = finished
    new_invoice.quantity = quantity
    new_invoice.time = time
    new_invoice.OS = OS
    if (targetVPS is not None):
        new_invoice.targetVPS = targetVPS
    new_invoice.save()


def createIP(type):
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    if type == 2:
        after = str(random.randint(200, 300)*100)
        ip += ":" + after
        return ip
    return ip


def checkIP(ip_need_check):
    ips = ip_need_check.split(':')
    if (len(ips) > 1):
        if VPS.objects.filter(ip=ips[0]).exclude(type=2).count() > 0:
            return False
        if VPS.objects.filter(ip=ip_need_check).filter(type=2).count() > 0:
            return False
    else:
        if VPS.objects.filter(ip__startswith=ip_need_check).count() > 0:
            return False
    return True


def createUsername():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))


def createPassword():
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    lowercase_char = random.choice(lowercase_letters)
    uppercase_char = random.choice(uppercase_letters)
    digit_char = random.choice(digits)
    special_char = random.choice(special_characters)

    remaining_chars = ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(4))

    password = ''.join(random.sample(
        lowercase_char + uppercase_char + digit_char + remaining_chars + special_char, 8))

    return password
