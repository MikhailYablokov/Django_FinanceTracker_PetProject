#task/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'amount', 'goal_type', 'due_date', 'currency']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'goal_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Название цели',
            'amount': 'Сумма',
            'goal_type': 'Тип цели',
            'due_date': 'Дата завершения',
            'currency': 'Валюта',
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше 0")
        return amount

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date and due_date < self.instance.created_date:
            raise forms.ValidationError("Дата завершения не может быть раньше даты создания")
        return due_date
