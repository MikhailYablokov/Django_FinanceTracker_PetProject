#transaction/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('edit_transaction/<int:id>/', views.TransactionEditView.as_view(), name='edit_transaction'),
    path('delete_transaction/<int:id>/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    path('delete_category/<int:id>/', views.CategoryDeleteView.as_view(), name='delete_category'),
]