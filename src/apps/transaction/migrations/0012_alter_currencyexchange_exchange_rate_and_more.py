# Generated by Django 5.1.7 on 2025-03-17 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_balance_updated_at_balance_user_transaction_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyexchange',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=6, max_digits=10, verbose_name='Курс обмена'),
        ),
        migrations.AlterField(
            model_name='currencyexchange',
            name='to_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
