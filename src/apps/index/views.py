from django.shortcuts import render, redirect
import locale
from datetime import datetime
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.transaction.models import Transaction
from apps.transaction.services import get_or_create_balances  # Оставляем для прогресса задач
from apps.task.models import Task

class HomeView(LoginRequiredMixin, View):
    """Дашборд"""
    login_url = '/authentication/login/'

    def get(self, request):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        current_date = datetime.today().strftime("%H:%M:%S %d %B %Y")

        transactions = Transaction.objects.filter(balance__user=request.user).order_by('-date')[:10]

        # Логика для целей
        search_query = request.GET.get('search', '')
        active_tasks = Task.objects.filter(completed=False)
        completed_tasks = Task.objects.filter(completed=True).order_by('-completed_date')

        if search_query:
            active_tasks = active_tasks.filter(title__icontains=search_query)

        active_tasks = active_tasks.order_by('-amount')
        # Расчёт прогресса задач
        balances = get_or_create_balances(request.user)
        for task in active_tasks:
            balance = balances[task.currency]
            task.progress = min(100, (float(balance.amount) / float(task.amount)) * 100) if task.amount else 0

        context = {
            'current_date': current_date,
            'transactions': transactions,
            'sort_by': 'date',
            'order': 'desc',
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'search': search_query,
        }
        return render(request, 'index/index.html', context)

    def post(self, request):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        current_date = datetime.today().strftime("%H:%M:%S %d %B %Y")
        transactions = Transaction.objects.filter(balance__user=request.user).order_by('-date')[:10]

        # Логика для целей
        search_query = request.GET.get('search', '')
        active_tasks = Task.objects.filter(completed=False)
        completed_tasks = Task.objects.filter(completed=True).order_by('-completed_date')

        if search_query:
            active_tasks = active_tasks.filter(title__icontains=search_query)

        active_tasks = active_tasks.order_by('-amount')
        # Расчёт прогресса задач
        balances = get_or_create_balances(request.user)
        for task in active_tasks:
            balance = balances[task.currency]
            task.progress = min(100, (float(balance.amount) / float(task.amount)) * 100) if task.amount else 0

        context = {
            'current_date': current_date,
            'transactions': transactions,
            'sort_by': 'date',
            'order': 'desc',
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'search': search_query,
        }
        return render(request, 'index/index.html', context)