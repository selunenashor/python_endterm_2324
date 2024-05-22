from django.contrib import admin
from .models import CustomUser, VPSTypeTemplate, VPSTemplate, VPS, Invoice, OSTemplate
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(VPSTypeTemplate)
admin.site.register(VPSTemplate)
admin.site.register(VPS)
admin.site.register(Invoice)
admin.site.register(OSTemplate)


