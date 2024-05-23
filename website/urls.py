from django.urls import path

from . import views

app_name = "shop"
urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("home", views.home, name="home"),
    path("order", views.orderStep1, name="order"),
    path("order/VPSType", views.orderStep2, name="order2"),
    path("order/os", views.orderStep3, name="order3"),
    path("order/confirm", views.orderConfirm, name="orderConfirm"),
    path("createVPS/<str:id>",views.createVPS,name="createVPS"),
    path("renewVPS/<str:id>",views.renewVPS,name="renewVPS"),
    path("VPSList", views.VPSList, name="VPSList"),
    path("invoiceList", views.invoiceList, name="invoiceList"),
    path("VPSDetail/<int:id>", views.VPSDetail, name="VPSDetail"),
    path("VPSStatusChange/<int:id>", views.changeVPSStatus, name="VPSStatusChange"),
    path("VPSRenewForm/<int:id>",views.renewVPSConfirm, name="VPSRenew"),
    path("VPSRenewComplete", views.invoice_renewVPS, name="VPSRenewComplete"),
    path("VPSDelete/<int:id>",views.deleteVPS, name="VPSDelete"),
    path("invoiceDetail/<str:id>", views.invoiceDetail, name="invoiceDetail"),
    path("invoiceCancel/<str:id>", views.cancelPayment, name="cancelPayment")
    
]
