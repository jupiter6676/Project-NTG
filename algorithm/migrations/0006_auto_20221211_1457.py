# Generated by Django 3.2.13 on 2022-12-11 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm', '0005_bjdata_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bjdata_di',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_di',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_go',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_go',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_pl',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_pl',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_ru',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_ru',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_si',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_si',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_total',
            name='tags',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bjdata_total',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
