# Generated by Django 2.2.13 on 2020-06-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20200613_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='amount_paid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
