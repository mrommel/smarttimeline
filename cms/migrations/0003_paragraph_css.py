# Generated by Django 3.0.4 on 2020-05-06 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20200505_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='css',
            field=models.CharField(choices=[('nor', ''), ('quo', 'blockquote blockquote-primary')], default='nor', max_length=3),
        ),
    ]
