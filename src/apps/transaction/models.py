from django.db import models
from django.contrib.auth.models import User


class Balance(models.Model):
    CURRENCY_TYPE_CHOICES = [
        ('RUB', '₽'),
        ('USD', '$'),
        ('EUR', '€'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=7, choices=CURRENCY_TYPE_CHOICES, default='RUB', verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Баланс: {self.amount} {self.currency}"

    def adjust_balance(self, amount_change, is_income=True):
        """Инкрементально изменяет баланс"""
        if is_income:
            self.amount += amount_change
        else:
            self.amount -= amount_change
        self.save()

    class Meta:
        unique_together = ('user', 'currency')


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='transaction')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='income')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount}"

    def save(self, *args, **kwargs):
        # Проверяем, это создание или обновление
        if self.pk is None:  # Новая транзакция
            super().save(*args, **kwargs)
            self.balance.adjust_balance(self.amount, is_income=(self.type == 'income'))
        else:  # Обновление существующей транзакции
            old_transaction = Transaction.objects.get(pk=self.pk)
            amount_change = self.amount - old_transaction.amount
            super().save(*args, **kwargs)
            if amount_change != 0:  # Если сумма изменилась
                self.balance.adjust_balance(
                    amount_change,
                    is_income=(self.type == 'income')
                )
            # Если тип изменился, корректируем баланс
            if self.type != old_transaction.type:
                # Отменяем старое влияние
                self.balance.adjust_balance(old_transaction.amount, is_income=(old_transaction.type == 'income'))
                # Применяем новое влияние
                self.balance.adjust_balance(self.amount, is_income=(self.type == 'income'))

    def delete(self, *args, **kwargs):
        # При удалении транзакции корректируем баланс
        self.balance.adjust_balance(self.amount, is_income=(self.type != 'income'))  # Обратная операция
        super().delete(*args, **kwargs)


class CurrencyExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='exchanges_from')
    to_balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='exchanges_to')
    from_amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Оставляем как вычисляемое
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Курс обмена")  # Пользователь вводит
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_amount} {self.from_balance.currency} -> {self.to_amount} {self.to_balance.currency}"

    def save(self, *args, **kwargs):
        # Вычисляем to_amount на основе введенного exchange_rate
        if not self.to_amount and self.exchange_rate:
            self.to_amount = self.from_amount * self.exchange_rate
        super().save(*args, **kwargs)