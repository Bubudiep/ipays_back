# Generated by Django 5.0.2 on 2024-07-16 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('file_type', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('img', models.TextField()),
                ('Comment', models.CharField(blank=True, default='', max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('fullname', models.CharField(blank=True, default='', max_length=100)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('adr_tinh', models.CharField(blank=True, default='', max_length=100)),
                ('adr_huyen', models.CharField(blank=True, default='', max_length=100)),
                ('adr_xa', models.CharField(blank=True, default='', max_length=100)),
                ('adr_details', models.CharField(blank=True, default='', max_length=100)),
                ('adr_full', models.CharField(blank=True, default='', max_length=300)),
                ('comment', models.CharField(blank=True, default='', max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
