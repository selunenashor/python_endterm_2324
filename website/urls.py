from django.urls import path

from . import views

app_name = "shop"
urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("home", views.home, name="home"),
    path("order", views.order, name="order"),
    path("VPSList", views.VPSList, name="VPSList"),
    path("invoiceList", views.invoiceList, name="invoiceList"),
    path("VPSDetail", views.VPSDetail, name="VPSDetail"),
    path("invoiceDetail", views.invoiceDetail, name="invoiceDetail"),
    path("invoiceConfirm",views.invoiceConfirm, name="invoiceConfirm")
]