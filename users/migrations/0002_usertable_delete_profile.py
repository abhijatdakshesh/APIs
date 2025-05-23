# Generated by Django 5.2.1 on 2025-05-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('aadhar_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('pan_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('residential_address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True)),
                ('total_experience_years', models.PositiveIntegerField(blank=True, null=True)),
                ('is_currently_working', models.BooleanField(default=False)),
                ('current_agencies', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
