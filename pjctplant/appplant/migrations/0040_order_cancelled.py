# Generated by Django 4.2.6 on 2024-03-18 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appplant', '0039_book_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
    ]