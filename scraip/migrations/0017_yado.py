# Generated by Django 2.2.2 on 2019-08-15 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraip', '0016_auto_20190810_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('yado_area', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': '宿名',
                'verbose_name_plural': '宿名',
                'db_table': 'yado',
            },
        ),
    ]