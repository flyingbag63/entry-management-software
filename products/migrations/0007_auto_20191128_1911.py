# Generated by Django 2.1.5 on 2019-11-28 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20191128_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='visitor_email',
            field=models.EmailField(max_length=254),
        ),
    ]
