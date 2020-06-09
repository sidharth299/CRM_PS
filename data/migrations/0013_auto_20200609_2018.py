# Generated by Django 2.2.13 on 2020-06-09 20:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_auto_20200609_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='hsn_code',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateField(default=django.utils.timezone.now)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('sample_quantity', models.PositiveIntegerField()),
                ('sample_status', models.CharField(choices=[('Sent', 'Sent'), ('Pending', 'Pending'), ('Passed', 'Passed'), ('Failed', 'Failed')], max_length=8)),
                ('remarks', models.CharField(blank=True, max_length=2000)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Client')),
                ('product_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('invoice_number', models.AutoField(primary_key=True, serialize=False)),
                ('sale_date', models.DateField(default=django.utils.timezone.now)),
                ('carting', models.PositiveIntegerField(default=0)),
                ('gstin', models.CharField(blank=True, max_length=15)),
                ('tax_type', models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Outside Maharashtra', 'Outside Maharashtra'), ('Indirect Export', 'Indirect Export'), ('Direct Export', 'Direct Export')], max_length=20)),
                ('is_sample', models.BooleanField(default=False)),
                ('total_amount', models.PositiveIntegerField()),
                ('amount_paid', models.PositiveIntegerField()),
                ('fisrt_date', models.DateField(default=django.utils.timezone.now)),
                ('last_date', models.DateField(default=django.utils.timezone.now)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount_received', models.PositiveIntegerField()),
                ('invoice_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Sales')),
            ],
        ),
        migrations.CreateModel(
            name='Dsr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_person', models.CharField(blank=True, max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contact_mode', models.CharField(choices=[('Visit', 'Visit'), ('Telephone', 'Telephone'), ('Email', 'Email'), ('WhatsApp', 'WhatsApp'), ('No Response', 'No Response'), ('Others', 'Others')], max_length=12)),
                ('date_of_contact', models.DateField(default=django.utils.timezone.now)),
                ('action', models.CharField(max_length=2000)),
                ('next_call_date', models.DateField()),
                ('sample_status', models.CharField(blank=True, choices=[('Sent', 'Sent'), ('Pending', 'Pending'), ('Passed', 'Passed'), ('Failed', 'Failed')], max_length=8)),
                ('client_rank', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)])),
                ('failed_sale', models.BooleanField(default=False)),
                ('successful_sale', models.BooleanField(default=False)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Client')),
                ('product_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='data.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_rate', models.PositiveIntegerField(blank=True)),
                ('quantity', models.PositiveIntegerField()),
                ('igst', models.DecimalField(decimal_places=2, max_digits=20)),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=20)),
                ('export_sale', models.DecimalField(decimal_places=2, max_digits=20)),
                ('invoice_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Sales')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.Product')),
            ],
        ),
    ]