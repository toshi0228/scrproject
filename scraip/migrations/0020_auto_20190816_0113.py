# Generated by Django 2.2.2 on 2019-08-16 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0019_auto_20190816_0104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='nam',
            new_name='name',
        ),
    ]
