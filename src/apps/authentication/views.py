# C:\PythonProjects\django\src\apps\authentication\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('/authentication/login/')  # Перенаправляем на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})