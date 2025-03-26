# task/models.py
from django.db import models


# Create your models here.
from django.db import models

class Task(models.Model):
    GOAL_TYPE_CHOICES = [
        ('payoff', 'Погасить долг'),
        ('save', 'Накопить'),
    ]
    CURRENCY_TYPE_CHOICES = [
        ('RUB', '₽'),
        ('USD', '$'),
        ('EUR', '€'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    goal_type = models.CharField(max_length=31, choices=GOAL_TYPE_CHOICES, default='save', verbose_name='Тип накопления')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    due_date = models.DateField(null=True, blank=True, verbose_name='Дата завершения')
    currency = models.CharField(max_length=7, choices=CURRENCY_TYPE_CHOICES, default='RUB', verbose_name="Валюта")
    completed = models.BooleanField(default=False, verbose_name='Завершено')
    completed_date = models.DateField(null=True, blank=True, verbose_name='Дата завершения')

    class Meta:
        verbose_name = 'Финансовая цель'
        verbose_name_plural = 'Финансовые цели'

    def __str__(self):
        return f"{self.title}: {self.amount} {self.currency}. {self.goal_type}"