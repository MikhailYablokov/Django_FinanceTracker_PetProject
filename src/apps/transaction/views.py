# apps/transaction/views.py
import locale
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction, Category, Balance, CurrencyExchange
from .forms import TransactionForm, CategoryForm, BalanceForm, CurrencyExchangeForm
from .services import get_or_create_balances, validate_and_save_entity, update_balance, perform_currency_exchange

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

class HomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'

    def get(self, request):
        balances = get_or_create_balances(request.user)
        is_editing = request.GET.get('edit') == 'true'
        currency = request.GET.get('currency')

        if is_editing and currency and currency in balances:
            balance_form = BalanceForm(instance=balances[currency])
        else:
            balance_form = BalanceForm()

        transaction_form = TransactionForm(user=request.user)
        category_form = CategoryForm()
        exchange_form = CurrencyExchangeForm(user=request.user)

        sort_by = request.GET.get("sort_by", "date")
        order = request.GET.get("order", "desc")
        sort_field = f"-{sort_by}" if order == "desc" else sort_by

        transactions = Transaction.objects.filter(balance__user=request.user).order_by(sort_field)
        categories = Category.objects.all()

        context = {
            "transaction_form": transaction_form,
            "transactions": transactions,
            "category_form": category_form,
            "categories": categories,
            "balance_form": balance_form,
            "balances": balances.values(),
            "exchange_form": exchange_form,
            "is_editing": is_editing,
            "selected_currency": currency if is_editing else None,
            "sort_by": sort_by,
            "order": order,
        }
        return render(request, "transaction/transaction.html", context)

    def post(self, request):
        balances = get_or_create_balances(request.user)

        if 'submit_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST, user=request.user)
            if validate_and_save_entity(transaction_form):
                messages.success(request, "Транзакция добавлена!")
                return redirect("home")

        elif 'submit_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if validate_and_save_entity(category_form):
                messages.success(request, "Категория добавлена!")
                return redirect("home")

        elif 'submit_balance' in request.POST:
            currency = request.POST.get('currency')
            if currency not in balances:
                messages.error(request, "Неверная валюта!")
                return redirect("home")
            balance_form = BalanceForm(request.POST, instance=balances[currency])
            if validate_and_save_entity(balance_form):
                messages.success(request, "Баланс обновлён!")
                return redirect("home")
            else:
                messages.error(request, "Ошибка при обновлении баланса!")
                context = self._get_context(request, balance_form=balance_form)
                return render(request, "transaction/transaction.html", context)

        elif 'submit_exchange' in request.POST:
            exchange_form = CurrencyExchangeForm(request.POST, user=request.user)
            if perform_currency_exchange(exchange_form, request.user):
                messages.success(request, "Обмен выполнен!")
                return redirect("home")
            else:
                messages.error(request, "Ошибка при обмене: недостаточно средств или неверные данные")
                context = self._get_context(request, exchange_form=exchange_form)
                return render(request, "transaction/transaction.html", context)

        return self.get(request)

    def _get_context(self, request, balance_form=None, exchange_form=None):
        balances = get_or_create_balances(request.user)
        is_editing = request.GET.get('edit') == 'true'
        currency = request.GET.get('currency')
        sort_by = request.GET.get("sort_by", "date")
        order = request.GET.get("order", "desc")
        sort_field = f"-{sort_by}" if order == "desc" else sort_by

        return {
            "transaction_form": TransactionForm(user=request.user),
            "transactions": Transaction.objects.filter(balance__user=request.user).order_by(sort_field),
            "category_form": CategoryForm(),
            "categories": Category.objects.all(),
            "balance_form": balance_form or BalanceForm(),
            "balances": balances.values(),
            "exchange_form": exchange_form or CurrencyExchangeForm(user=request.user),
            "is_editing": is_editing,
            "selected_currency": currency if is_editing else None,
            "sort_by": sort_by,
            "order": order,
        }


class TransactionDeleteView(LoginRequiredMixin, View):
    """Удаление транзакции"""
    login_url = '/login/'

    def get(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, balance__user=request.user)
        transaction.delete()
        messages.success(request, "Транзакция удалена!")
        return redirect("home")


class CategoryDeleteView(LoginRequiredMixin, View):
    """Удаление категории"""
    login_url = '/login/'

    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        messages.success(request, "Категория удалена!")
        return redirect("home")


class TransactionEditView(LoginRequiredMixin, View):
    """Редактирование транзакции"""
    login_url = '/login/'

    def get(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, balance__user=request.user)
        form = TransactionForm(instance=transaction, user=request.user)
        return render(request, "transaction/edit_transaction.html", {"form": form})

    def post(self, request, id):
        transaction = get_object_or_404(Transaction, id=id, balance__user=request.user)
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if validate_and_save_entity(form):
            messages.success(request, "Транзакция обновлена!")
            return redirect("home")
        return render(request, "transaction/edit_transaction.html", {"form": form})