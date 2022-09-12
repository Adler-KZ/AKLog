# Generated by Django 4.1 on 2022-08-24 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_ipaddress_ip'),
        ('blogs', '0004_blog_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='hits',
            field=models.ManyToManyField(related_name='blogs', through='blogs.BlogIp', to='accounts.ipaddress', verbose_name='Hits'),
        ),
        migrations.AlterField(
            model_name='blogip',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.blog'),
        ),
        migrations.AlterField(
            model_name='blogip',
            name='ip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ipaddress'),
        ),
    ]