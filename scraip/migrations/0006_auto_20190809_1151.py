# Generated by Django 2.2.2 on 2019-08-09 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0005_auto_20190809_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='total_review',
            field=models.FloatField(default=0),
        ),
    ]
