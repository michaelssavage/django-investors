# Generated by Django 5.0.3 on 2024-03-29 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashCall',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_amount', models.DecimalField(decimal_places=0, max_digits=12)),
                ('IBAN', models.CharField(max_length=100)),
                ('email_send', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField()),
                ('invoice_status', models.CharField(choices=[('Pending', 'Pending'), ('Validated', 'Validated'), ('Sent', 'Sent'), ('Paid', 'Paid'), ('Overdue', 'Overdue')], default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('credit', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('startup_name', models.CharField(max_length=100)),
                ('invested_amount', models.DecimalField(decimal_places=0, max_digits=12)),
                ('percentage_fees', models.DecimalField(decimal_places=0, max_digits=2)),
                ('date_added', models.DateTimeField()),
                ('fees_type', models.CharField(choices=[('upfront', 'Upfront'), ('yearly', 'Yearly')], max_length=10)),
                ('investor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.investor')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fees_amount', models.DecimalField(decimal_places=0, max_digits=12)),
                ('date_added', models.DateTimeField()),
                ('fees_type', models.CharField(choices=[('upfront', 'Upfront'), ('yearly', 'Yearly')], max_length=20)),
                ('investment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.investment')),
                ('investor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.investor')),
            ],
        ),
    ]