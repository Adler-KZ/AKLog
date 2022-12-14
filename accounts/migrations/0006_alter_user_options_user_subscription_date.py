# Generated by Django 4.1 on 2022-09-05 12:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_is_author_user_bio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_see_vip', 'Can see vip blogs')]},
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
