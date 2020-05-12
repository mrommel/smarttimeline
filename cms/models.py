from django.db import models
from django.utils.translation import gettext_lazy as _


class Content(models.Model):
    title = models.CharField(max_length=50)

    def paragraphs(self):
        return Paragraph.objects.filter(content=self)

    # ...
    def __str__(self):
        return self.title


class ParagraphCss(models.TextChoices):
    NORMAL = 'nor', _('Normal')
    QUOTE = 'quo', _('Quote') # blockquote blockquote-blue
    INFO = 'inf', _('Info') # text-info


class Paragraph(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    headline = models.CharField(max_length=100)
    text = models.CharField(max_length=2048)
    css = models.CharField(max_length=3, choices=ParagraphCss.choices, default=ParagraphCss.NORMAL, )


    def cssSytle(self):
        if self.css == ParagraphCss.NORMAL:
            return ""

        if self.css == ParagraphCss.QUOTE:
            return "blockquote blockquote-blue"

        if self.css == ParagraphCss.INFO:
            return "text-info"

        return ""


    # ...
    def __str__(self):
        return "%s - %s" % (self.content.title, self.headline)
