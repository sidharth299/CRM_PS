# Generated by Django 2.2.13 on 2020-06-11 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='zone',
            field=models.CharField(blank=True, choices=[('NORTH', 'NORTH'), ('SOUTH', 'SOUTH'), ('EAST', 'EAST'), ('WEST', 'WEST'), ('CENTRAL', 'CENTRAL'), ('EXPORT', 'EXPORT'), ('NAGPUR', 'NAGPUR')], default='NAGPUR', max_length=8),
        ),
    ]
