# Generated by Django 5.1.7 on 2025-03-16 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='currency',
            field=models.CharField(choices=[('RUB', '₽'), ('USD', '$'), ('EUR', '€')], default='RUB', max_length=7, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='task',
            name='goal_type',
            field=models.CharField(choices=[('payoff', 'Погасить долг'), ('save', 'Накопить')], default='save', max_length=31, verbose_name='Тип накопления'),
        ),
    ]
