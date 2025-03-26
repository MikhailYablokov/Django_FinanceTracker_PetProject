# apps/transaction/services.py
from django.db import transaction
from .models import Balance, CurrencyExchange

def get_or_create_balances(user):
    currencies = [choice[0] for choice in Balance.CURRENCY_TYPE_CHOICES]
    balances = {}
    for currency in currencies:
        balance, _ = Balance.objects.get_or_create(
            user=user,
            currency=currency,
            defaults={'amount': 0}
        )
        balances[currency] = balance
    return balances

def validate_and_save_entity(form):
    if form.is_valid():
        form.save()
        return True
    return False

def update_balance(form, balance):
    if form.is_valid():
        form.save()
        return True
    return False

def perform_currency_exchange(form, user):
    if not form.is_valid():
        return False

    exchange = form.save(commit=False)
    exchange.user = user

    # Определяем направление обмена и вычисляем to_amount
    from_currency = exchange.from_balance.currency
    to_currency = exchange.to_balance.currency
    exchange_rate = exchange.exchange_rate

    if from_currency == 'RUB' and to_currency == 'USD':
        # Курс: сколько RUB за 1 USD, делим RUB на курс
        exchange.to_amount = exchange.from_amount / exchange_rate
    elif from_currency == 'USD' and to_currency == 'RUB':
        # Курс: сколько RUB за 1 USD, умножаем USD на курс
        exchange.to_amount = exchange.from_amount * exchange_rate
    elif from_currency == 'RUB' and to_currency == 'EUR':
        # Курс: сколько RUB за 1 EUR, делим RUB на курс
        exchange.to_amount = exchange.from_amount / exchange_rate
    elif from_currency == 'EUR' and to_currency == 'RUB':
        # Курс: сколько RUB за 1 EUR, умножаем EUR на курс
        exchange.to_amount = exchange.from_amount * exchange_rate
    elif from_currency == 'USD' and to_currency == 'EUR':
        # Курс: сколько USD за 1 EUR, делим USD на курс
        exchange.to_amount = exchange.from_amount / exchange_rate
    elif from_currency == 'EUR' and to_currency == 'USD':
        # Курс: сколько USD за 1 EUR, умножаем EUR на курс
        exchange.to_amount = exchange.from_amount * exchange_rate
    else:
        return False  # Неподдерживаемая пара валют

    with transaction.atomic():
        exchange.from_balance.adjust_balance(exchange.from_amount, is_income=False)
        exchange.to_balance.adjust_balance(exchange.to_amount, is_income=True)
        exchange.save()
    return True