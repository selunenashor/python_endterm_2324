from django.db import models


class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(max_length=100, unique=True)
    password = models.TextField(max_length=100)
    email = models.EmailField()
    phone = models.TextField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f'({self.username})'


class VPSTypeTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'({self.name})'


class VPSTemplate(models.Model):
    id = models.TextField(primary_key=True)
    type = models.ForeignKey(VPSTypeTemplate, on_delete=models.CASCADE)
    CPU = models.IntegerField()
    RAM = models.IntegerField()
    SSD = models.IntegerField()
    pricePerMonth = models.IntegerField()

    def __str__(self) -> str:
        return f'({self.id})'


class OSTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'({self.name})'


class VPS(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=50)
    plan = models.CharField(max_length=10)
    CPU = models.IntegerField()
    RAM = models.IntegerField()
    SSD = models.IntegerField()
    OS = models.ForeignKey(OSTemplate, on_delete=models.CASCADE)
    price = models.IntegerField()
    expired_date = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.IntegerField()

    def __str__(self) -> str:
        return f'({self.ip})'


class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'({self.name})'


class Invoice(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    id_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.IntegerField()
    price = models.IntegerField()
    VPSType = models.CharField(max_length=200)
    status = models.IntegerField()
    paymentMethod = models.CharField(max_length=100)
    createAt = models.DateTimeField()
    finished = models.DateTimeField()
    targetVPS = models.CharField(max_length=20, null=True)
    quantity = models.IntegerField()
    time = models.IntegerField()
    OS = models.IntegerField()

    def __str__(self) -> str:
        return f'({self.id})'
