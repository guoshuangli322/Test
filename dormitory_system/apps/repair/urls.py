from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.RepairListView.as_view(), name='repair_list'),
    path('create/', views.RepairCreateView.as_view(), name='repair_create'),
    path('<int:pk>/', views.RepairDetailView.as_view(), name='repair_detail'),
    path('<int:pk>/process/', views.RepairProcessView.as_view(), name='repair_process'),
    path('my/', views.MyRepairView.as_view(), name='my_repairs'),
]
