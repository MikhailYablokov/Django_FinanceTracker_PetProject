# config/urls.py
from django.contrib import admin
from django.urls import path, include

handler404 = 'config.views.invalid_page'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.index.urls')),
    path('tasks/', include('apps.task.urls')),
    path('transactions/', include('apps.transaction.urls')),
    path('authentication/', include('apps.authentication.urls')),
]