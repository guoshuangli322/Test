from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogListView.as_view(), name='log_list'),
    path('export/', views.ExportLogsView.as_view(), name='log_export'),
]
