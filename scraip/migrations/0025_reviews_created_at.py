# Generated by Django 2.2.2 on 2019-08-19 04:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0024_auto_20190819_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時'),
        ),
    ]
