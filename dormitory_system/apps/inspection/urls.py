from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.InspectionListView.as_view(), name='inspection_list'),
    path('add/', views.InspectionCreateView.as_view(), name='inspection_add'),
    path('<int:pk>/', views.InspectionDetailView.as_view(), name='inspection_detail'),
    path('statistics/', views.InspectionStatisticsView.as_view(), name='inspection_stats'),
]
