# Generated by Django 2.2.2 on 2019-08-19 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0020_auto_20190816_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yado',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='宿の名前'),
        ),
        migrations.AlterField(
            model_name='yado',
            name='yado_area',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
