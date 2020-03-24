from django.contrib import admin
from .models import App, Version, Rating

admin.site.register(App)
admin.site.register(Version)
admin.site.register(Rating)