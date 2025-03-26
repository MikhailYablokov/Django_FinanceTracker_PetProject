from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from datetime import date
from .forms import TaskForm
from .models import Task
from apps.transaction.services import get_or_create_balances  # Оставляем для прогресса
from django.urls import reverse

class HomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login/'

    def _get_context_data(self, request, task_form=None):
        task_form = task_form or TaskForm()
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

        return {
            'task_form': task_form,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'search': search_query,
        }

    def get(self, request):
        context = self._get_context_data(request)
        return render(request, 'task/task.html', context)

    def post(self, request):
        if 'submit_task' in request.POST:
            task_form = TaskForm(request.POST)
            if task_form.is_valid():  # Заменил validate_and_save_entity на стандартную проверку
                task_form.save()
                messages.success(request, "Цель добавлена!")
                return redirect('tasks_home')
            context = self._get_context_data(request, task_form=task_form)
            return render(request, 'task/task.html', context)

        return self.get(request)

class TaskListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '-amount')
        tasks = Task.objects.all()

        if search_query:
            tasks = tasks.filter(title__icontains=search_query)

        if sort_by:
            tasks = tasks.order_by(sort_by)

        # Расчёт прогресса задач
        balances = get_or_create_balances(request.user)
        for task in tasks:
            if not task.completed:
                balance = balances[task.currency]
                task.progress = min(100, (float(balance.amount) / float(task.amount)) * 100) if task.amount else 0

        context = {
            'tasks': tasks,
            'sort_by': sort_by,
            'search': search_query,
        }
        return render(request, 'task/task_list.html', context)

class TaskEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        task = get_object_or_404(Task, id=id, completed=False)
        form = TaskForm(instance=task)
        return render(request, 'task/edit_task.html', {'form': form, 'task': task})

    def post(self, request, id):
        task = get_object_or_404(Task, id=id, completed=False)
        form = TaskForm(request.POST, instance=task)
        next_url = request.GET.get('next', reverse('tasks_home'))
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '-amount')

        redirect_url = next_url
        if search_query:
            redirect_url += f'?search={search_query}'
        if 'task_list' in next_url and sort_by:
            redirect_url += f'&sort_by={sort_by}' if search_query else f'?sort_by={sort_by}'

        if form.is_valid():  # Заменил validate_and_save_entity
            form.save()
            messages.success(request, "Цель обновлена!")
            return redirect(redirect_url)
        return render(request, 'task/edit_task.html', {'form': form, 'task': task})

class TaskDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)
        next_url = request.GET.get('next', reverse('tasks_home'))
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '-amount')

        redirect_url = next_url
        if search_query:
            redirect_url += f'?search={search_query}'
        if 'task_list' in next_url and sort_by:
            redirect_url += f'&sort_by={sort_by}' if search_query else f'?sort_by={sort_by}'

        task.delete()
        messages.success(request, "Цель удалена!")
        return redirect(redirect_url)

class TaskCompleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        task = get_object_or_404(Task, id=id, completed=False)
        balances = get_or_create_balances(request.user)
        balance = balances[task.currency]
        next_url = request.GET.get('next', reverse('tasks_home'))
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '-amount')

        redirect_url = next_url
        if search_query:
            redirect_url += f'?search={search_query}'
        if 'task_list' in next_url and sort_by:
            redirect_url += f'&sort_by={sort_by}' if search_query else f'?sort_by={sort_by}'

        if balance.amount < task.amount:
            messages.error(request, f"Недостаточно средств на балансе {task.currency} для завершения цели '{task.title}'!")
            return redirect(redirect_url)

        with transaction.atomic():
            balance.adjust_balance(task.amount, is_income=False)
            task.completed = True
            task.completed_date = date.today()
            task.save()

        messages.success(request, f"Цель '{task.title}' завершена!")
        return redirect(redirect_url)