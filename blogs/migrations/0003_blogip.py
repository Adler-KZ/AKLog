# Generated by Django 4.1 on 2022-08-24 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_ipaddress'),
        ('blogs', '0002_alter_blog_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_ip', to='blogs.blog', verbose_name='Blog')),
                ('ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_ip', to='accounts.ipaddress', verbose_name='Ip address')),
            ],
        ),
    ]
