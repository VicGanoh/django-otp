# Generated by Django 5.0.4 on 2024-04-11 22:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('72faf0a5-2a21-420e-b6ac-7caa0bded62c'), editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('60298dd1-35ca-42a3-a6cb-fd5dd56fffe0'), editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('otp_code', models.CharField(blank=True, default='', max_length=6, verbose_name='OTP code')),
                ('secret_key', models.CharField(blank=True, max_length=50, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'OTP Verification',
                'verbose_name_plural': 'OTP Verifications',
            },
        ),
    ]