# Generated by Django 5.2.1 on 2025-05-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usertable_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertable',
            name='full_name',
        ),
        migrations.AddField(
            model_name='usertable',
            name='first_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='usertable',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
