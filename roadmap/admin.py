from django.contrib import admin

# Register your models here.
from roadmap.models import Item, Lane, Plan

admin.site.register(Plan)
admin.site.register(Lane)
admin.site.register(Item)