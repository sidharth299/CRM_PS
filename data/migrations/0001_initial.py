# Generated by Django 2.2.13 on 2020-06-07 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=50, unique=True)),
                ('gstin', models.CharField(blank=True, max_length=15)),
                ('client_category', models.CharField(choices=[('Agrochem', 'Agrochem'), ('Construction', 'Construction'), ('Others', 'Others')], max_length=15)),
                ('btc', models.CharField(blank=True, choices=[('Non BTC', 'Non BTC'), ('BTC-1', 'BTC-1'), ('BTC-2', 'BTC-2')], max_length=7)),
                ('telephone_main', models.CharField(blank=True, max_length=15)),
                ('telephone_extra', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contact_person', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=400)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('pin_code', models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(100000), django.core.validators.MaxValueValidator(999999)])),
                ('state', models.CharField(blank=True, choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh ', 'Arunachal Pradesh '), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Delhi', 'Delhi'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Ladakh', 'Ladakh'), ('Lakshadweep', 'Lakshadweep'), ('Puducherry', 'Puducherry')], default='Maharashtra', max_length=30)),
                ('country', models.CharField(blank=True, choices=[('India', 'India'), ('Overseas', 'Overseas')], default='India', max_length=8)),
                ('client_rank', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('lead_source', models.CharField(choices=[('Reference', 'Reference'), ('Indiamart', 'Indiamart'), ('Others', 'Others')], max_length=9)),
                ('remarks', models.CharField(blank=True, max_length=2000)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('latest_dsr_id', models.PositiveIntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_category', models.CharField(choices=[('Agro Chemical', 'Agro Chemical'), ('Defoamer Chemical', 'Defoamer Chemical'), ('Textil Industry Chemical', 'Textil Industry Chemical'), ('Cosmetics Industry Chemical', 'Cosmetics Industry Chemical'), ('Construction Chemical', 'Construction Chemical'), ('Mining Insutry Chemical', 'Mining Insutry Chemical'), ('Paper Insutry Chemical', 'Paper Insutry Chemical'), ('Others', 'Others')], max_length=30)),
                ('hsn_code', models.PositiveIntegerField(blank=True)),
                ('basic_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('export_tax_rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('remarks', models.CharField(blank=True, max_length=2000)),
            ],
        ),
    ]
