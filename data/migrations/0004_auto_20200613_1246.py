# Generated by Django 2.2.13 on 2020-06-13 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20200611_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='fisrt_date',
            new_name='first_date',
        ),
    ]
