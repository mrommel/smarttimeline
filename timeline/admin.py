from django.contrib import admin

from .models import App, Version, Rating
from .form import VersionModelForm


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    fields = ('pub_date', 'rating')


class VersionInline(admin.TabularInline):
    form = VersionModelForm
    model = Version
    extra = 1


class AppAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Mobile OS', {'fields': ['mobile_os'], 'classes': ['collapse']}),
        ('Style', {'fields': ['color', 'solid'], 'classes': ['collapse']}),
    ]
    inlines = [RatingInline, VersionInline, ]


admin.site.register(App, AppAdmin)
admin.site.register(Version)
admin.site.register(Rating)

admin.site.site_header = "MiRo Admin"