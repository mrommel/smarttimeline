import datetime

from colorfield.fields import ColorField
from django.db import models


def add_one_month(orig_date):
    # advance year and month by one month
    new_year = orig_date.year
    new_month = orig_date.month + 1
    # note: in datetime.date, months go from 1 to 12
    if new_month > 12:
        new_year += 1
        new_month -= 12

    new_day = orig_date.day
    # while day is out of range for month, reduce by one
    while True:
        try:
            new_date = datetime.date(new_year, new_month, new_day)
        except ValueError as e:
            new_day -= 1
        else:
            break

    return new_date


class Plan(models.Model):
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=512)
    start_date = models.DateField('date started')
    end_date = models.DateField('date ended')

    # ...
    def months(self):
        month_list = []

        current_date = self.start_date

        while current_date < self.end_date:
            year_str = "%s" % (current_date.year - 2000)
            month_str = "%s" % current_date.strftime("%B")
            combined_str = "%s%s" % (month_str[:3], year_str[:2])
            month_list.append(combined_str)
            current_date = add_one_month(current_date)

        return month_list

    # ...
    def lanes(self):
        return Lane.objects.filter(plan=self)

    # ...
    def __str__(self):
        return "%s" % (self.name)


class Lane(models.Model):
    name = models.CharField(max_length=200)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    color = ColorField(default='#000000')

    def background_color(self):
        # h = tuple(int(self.color[i:i + 2], 16) for i in (0, 2, 4)))

        return "%s66" % self.color

    # ...
    def items(self):
        return Item.objects.filter(lane=self)

    # ...
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    start_date = models.DateField('date started')
    end_date = models.DateField('date ended')

    def start_date_str(self):
        year_str = "%s" % (self.start_date.year - 2000)
        month_str = "%s" % self.start_date.strftime("%B")
        combined_str = "%s%s" % (month_str[:3], year_str[:2])
        return combined_str

    def end_date_str(self):
        year_str = "%s" % (self.end_date.year - 2000)
        month_str = "%s" % self.end_date.strftime("%B")
        combined_str = "%s%s" % (month_str[:3], year_str[:2])
        return combined_str

    # ...
    def __str__(self):
        return "%s (%s)" % (self.name, self.lane)
