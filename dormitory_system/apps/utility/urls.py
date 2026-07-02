from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.UtilityBillListView.as_view(), name='utility_list'),
    path('add/', views.UtilityBillCreateView.as_view(), name='utility_add'),
    path('<int:pk>/edit/', views.UtilityBillUpdateView.as_view(), name='utility_edit'),
    path('<int:pk>/pay/', views.UtilityBillPayView.as_view(), name='utility_pay'),
    path('export/', views.ExportUtilityView.as_view(), name='utility_export'),
]
