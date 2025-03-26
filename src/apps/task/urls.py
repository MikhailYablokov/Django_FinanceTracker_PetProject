from django.urls import path
from .views import HomeView, TaskEditView, TaskDeleteView, TaskCompleteView, TaskListView

urlpatterns = [
    path('', HomeView.as_view(), name='tasks_home'),
    path('edit/<int:id>/', TaskEditView.as_view(), name='edit_task'),
    path('delete/<int:id>/', TaskDeleteView.as_view(), name='delete_task'),
    path('complete/<int:id>/', TaskCompleteView.as_view(), name='complete_task'),
    path('list/', TaskListView.as_view(), name='task_list'),
]