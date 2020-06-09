# Generated by Django 2.2.13 on 2020-06-09 11:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20200607_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_category',
            field=models.CharField(choices=[('A', 'Agrochem'), ('Construction', 'Construction'), ('Others', 'Others')], max_length=15),
        ),
        migrations.CreateModel(
            name='Dsr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_person', models.CharField(blank=True, max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contact_mode', models.CharField(choices=[('V', 'Visit'), ('T', 'Telephone'), ('E', 'Email'), ('WA', 'WhatsApp'), ('NR', 'No Response'), ('O', 'Others')], max_length=9)),
                ('date_of_contact', models.DateField()),
                ('action', models.CharField(max_length=2000)),
                ('next_call_date', models.DateField()),
                ('sample_status', models.CharField(choices=[('Reference', 'Reference'), ('Indiamart', 'Indiamart'), ('Others', 'Others')], max_length=9)),
                ('client_rank', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('failed_sale', models.BooleanField(default=False)),
                ('successful_sale', models.BooleanField(default=False)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Client')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Product')),
            ],
        ),
    ]