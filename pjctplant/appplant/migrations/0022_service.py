# Generated by Django 4.2.6 on 2024-02-28 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appplant', '0021_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]