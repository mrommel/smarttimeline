from django.contrib import admin

from .form import ParagraphModelForm
from .models import Content, Paragraph


class ParagraphInline(admin.TabularInline):
    form = ParagraphModelForm
    model = Paragraph
    extra = 1


class ContentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Title', {'fields': ['title']}),
    ]
    inlines = [ParagraphInline, ]


admin.site.register(Content, ContentAdmin)
admin.site.register(Paragraph)
