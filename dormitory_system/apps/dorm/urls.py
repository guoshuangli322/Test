from django.urls import path
from . import views

urlpatterns = [
    path('buildings/', views.BuildingListView.as_view(), name='building_list'),
    path('buildings/add/', views.BuildingCreateView.as_view(), name='building_add'),
    path('buildings/<int:pk>/edit/', views.BuildingUpdateView.as_view(), name='building_edit'),
    path('buildings/<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='building_delete'),
    path('buildings/<int:pk>/rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/add/', views.RoomCreateView.as_view(), name='room_add'),
    path('rooms/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
    path('rooms/<int:pk>/beds/', views.BedListView.as_view(), name='bed_list'),
    path('beds/add/', views.BedCreateView.as_view(), name='bed_add'),
    path('beds/<int:pk>/edit/', views.BedUpdateView.as_view(), name='bed_edit'),
    path('beds/<int:pk>/delete/', views.BedDeleteView.as_view(), name='bed_delete'),
    # 批量生成房间和床位
    path('batch-create/', views.BatchCreateView.as_view(), name='batch_create'),
]
