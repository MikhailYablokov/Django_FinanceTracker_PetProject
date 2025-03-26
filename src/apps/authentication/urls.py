# C:\PythonProjects\django\src\apps\authentication\urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Импортируем ваши кастомные представления

app_name = 'authentication'

urlpatterns = [
    # Вход
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    # Выход
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Регистрация
    path('register/', views.register, name='register'),
]