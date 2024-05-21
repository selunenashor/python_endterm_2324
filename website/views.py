from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def order(request):
    return render(request, "order.html")

def VPSList(request): 
    return render(request, 'VPSList.html')

def invoiceList(request):
    return render(request, 'invoiceList.html')

def VPSDetail(request):
    return render(request, 'VPSDetail.html')

def invoiceDetail(request):
    return render(request, 'invoiceDetail.html')

def invoiceConfirm(request):
    return render(request, 'invoiceConfirm.html')