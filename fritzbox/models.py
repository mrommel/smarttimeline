from django.db import models


class BoxConfig(models.Model):
    address = models.CharField(max_length=16)
    user = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return "%s (%s)" % (self.address, self.user)