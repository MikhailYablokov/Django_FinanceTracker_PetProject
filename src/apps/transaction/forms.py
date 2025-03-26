# transaction/forms.py
from django import forms
from django.utils import timezone
from .models import Transaction, Category, Balance, CurrencyExchange


class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = 'Сумма'


class TransactionForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label='Тип транзакции',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    balance = forms.ModelChoiceField(
        queryset=Balance.objects.none(),
        label='Баланс',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = ['balance', 'type', 'category', 'amount', 'description', 'date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['balance'].queryset = Balance.objects.filter(user=user)

        if not self.instance.pk:
            self.initial['date'] = timezone.now().date()

        self.fields['category'].label = 'Категория'
        self.fields['amount'].label = 'Сумма'
        self.fields['description'].label = 'Описание'
        self.fields['date'].label = 'Дата'

    def clean(self):
        cleaned_data = super().clean()
        balance = cleaned_data.get('balance')
        amount = cleaned_data.get('amount')
        transaction_type = cleaned_data.get('type')

        if balance and amount and transaction_type == 'expense':
            if balance.amount < amount:
                raise forms.ValidationError(
                    f"Недостаточно средств на балансе {balance.currency} для расхода"
                )
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название категории'


class CurrencyExchangeForm(forms.ModelForm):
    class Meta:
        model = CurrencyExchange
        fields = ['from_balance', 'to_balance', 'from_amount', 'exchange_rate']
        widgets = {
            'from_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'exchange_rate': forms.NumberInput(attrs={'step': '0.000001'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['from_balance'].queryset = Balance.objects.filter(user=user)
            self.fields['to_balance'].queryset = Balance.objects.filter(user=user)
        self.fields['from_balance'].label = 'Исходный баланс'
        self.fields['to_balance'].label = 'Целевой баланс'
        self.fields['from_amount'].label = 'Сумма обмена'
        self.fields['exchange_rate'].label = 'Курс обмена'

    def clean(self):
        cleaned_data = super().clean()
        from_balance = cleaned_data.get('from_balance')
        to_balance = cleaned_data.get('to_balance')
        from_amount = cleaned_data.get('from_amount')
        exchange_rate = cleaned_data.get('exchange_rate')

        if from_balance and to_balance and from_amount and exchange_rate:
            if from_balance == to_balance:
                raise forms.ValidationError("Нельзя обменивать валюту на ту же валюту.")
            if from_amount <= 0 or exchange_rate <= 0:
                raise forms.ValidationError("Сумма и курс обмена должны быть положительными.")
            if from_amount > from_balance.amount:
                raise forms.ValidationError("Недостаточно средств на исходном балансе.")
        return cleaned_data