# Generated by Django 3.2.13 on 2022-12-09 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0004_studynotice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studynotice',
            name='study',
        ),
    ]
