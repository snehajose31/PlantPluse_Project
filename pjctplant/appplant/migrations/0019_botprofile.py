# Generated by Django 4.2.6 on 2024-02-12 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appplant', '0018_doctorschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('pincode', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('specification', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
