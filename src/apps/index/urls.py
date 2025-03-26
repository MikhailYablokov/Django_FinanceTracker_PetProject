# C:\PythonProjects\django\src\apps\index\urls.py
from django.urls import path
from . import views

app_name = 'index'  # Пространство имен для index

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Главная страница
]