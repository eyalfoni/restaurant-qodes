from django.conf import settings
from django.db import models


class QRCode(models.Model):
    # columns
    forwarding_url = models.URLField()
    qr_code_img = models.ImageField()

    # relationships
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
