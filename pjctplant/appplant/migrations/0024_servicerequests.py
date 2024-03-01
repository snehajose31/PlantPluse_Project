# Generated by Django 4.2.6 on 2024-02-28 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appplant', '0023_servicerequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirm', 'Confirmed'), ('complete', 'Complete')], default='pending', max_length=20)),
                ('bot_profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appplant.botprofile')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appplant.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
