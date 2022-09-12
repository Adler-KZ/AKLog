# Generated by Django 4.1 on 2022-09-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_remove_comment_username_comment_email_comment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Full name'),
        ),
    ]
