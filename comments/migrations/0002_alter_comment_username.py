# Generated by Django 4.1 on 2022-08-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(max_length=50, verbose_name='Username'),
        ),
    ]
