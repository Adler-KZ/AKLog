# Generated by Django 4.1 on 2022-09-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_ipaddress_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_author',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=250, verbose_name='Bio'),
        ),
    ]
