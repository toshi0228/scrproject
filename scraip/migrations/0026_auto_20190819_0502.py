# Generated by Django 2.2.2 on 2019-08-19 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0025_reviews_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='投稿日時'),
        ),
    ]