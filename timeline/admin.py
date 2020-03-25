from django.contrib import admin
from django import forms

from .models import App, Version, Rating


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 1


class VersionModelForm(forms.ModelForm):
    changelog = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Version
        fields = ['name', 'changelog', 'pub_date', ]


class VersionInline(admin.StackedInline):
    form = VersionModelForm
    model = Version
    extra = 1


class AppAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Mobile OS', {'fields': ['mobile_os'], 'classes': ['collapse']}),
    ]
    inlines = [RatingInline, VersionInline, ]


admin.site.register(App, AppAdmin)
admin.site.register(Version)
admin.site.register(Rating)