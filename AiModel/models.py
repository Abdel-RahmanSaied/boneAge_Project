from django.db import models
from django.conf import settings
# Create your models here.

class Xray(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    patient_name = models.CharField(max_length=30, null=False, blank=False)
    image = models.ImageField(upload_to='xray_images', null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    result = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return str(self.id) + " - " + str(self.user)
