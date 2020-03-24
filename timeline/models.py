from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class MobileOS(models.TextChoices):
    ANDROID = 'And', _('Android')
    IOS = 'iOS', _('iOS')


class App(models.Model):
    name = models.CharField(max_length=200)
    mobile_os = models.CharField(max_length=3, choices=MobileOS.choices, default=MobileOS.ANDROID, )

    # ...
    def __str__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    changelog = models.CharField(max_length=200)
    pub_date = models.DateField('date published')

    # ...
    def __str__(self):
        return self.name


class Rating(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    pub_date = models.DateField('date published')
    
    # ...
    def __str__(self):
        return 'Bewertung %s vom %s' % (self.app.name, self.pub_date)