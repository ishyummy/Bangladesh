from django.db import models
from account.models import User


class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    CP = models.CharField(max_length=50, null=False)
    CPD = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=50, null=False)
    mobile = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, null=False)
    SCP = models.CharField(max_length=50, null=True)
    SCPMN = models.CharField(max_length=50, null=True)
    SCPD = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    reference = models.CharField(max_length=50, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name