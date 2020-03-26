from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from datetime import date

# Create your models here.

class MobileOS(models.TextChoices):
    ANDROID = 'And', _('Android')
    IOS = 'iOS', _('iOS')


def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)


class App(models.Model):
    name = models.CharField(max_length=200)
    mobile_os = models.CharField(max_length=3, choices=MobileOS.choices, default=MobileOS.ANDROID, )
    color = ColorField(default='#000000')
    solid = models.BooleanField(default=True)

    def current_version(self):
        return Version.objects.filter(app=self).latest('pub_date')

    def current_rating(self):
        return Rating.objects.filter(app=self).latest('pub_date')

    def last_month_rating(self):
        all_ratings = Rating.objects.filter(app=self).order_by('pub_date')
        last_month = monthdelta(date.today(), -1)
        return next((x for x in all_ratings if x.pub_date > last_month), None)

    def last_month_delta_rating(self):

        curr = self.current_rating()
        last = self.last_month_rating()

        if curr is not None and last is not None:
            return curr.rating - last.rating

        return 0.0

    # ...
    def __str__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(max_length=200)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    changelog = models.CharField(max_length=512)
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