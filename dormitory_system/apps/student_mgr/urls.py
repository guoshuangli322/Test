from django.urls import path
from . import views

urlpatterns = [
    # 学生信息管理
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('add/', views.StudentCreateView.as_view(), name='student_add'),
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('<int:pk>/detail/', views.StudentDetailView.as_view(), name='student_detail'),

    # 入住/调宿/退宿
    path('<int:pk>/checkin/', views.CheckInView.as_view(), name='student_checkin'),
    path('<int:pk>/change-room/', views.ChangeRoomView.as_view(), name='student_change_room'),
    path('<int:pk>/checkout/', views.CheckOutView.as_view(), name='student_checkout'),

    # 住宿记录
    path('records/', views.DormRecordListView.as_view(), name='dorm_record_list'),

    # 历史记录
    path('history/', views.ChangeHistoryView.as_view(), name='change_history'),

    # Excel批量导入导出
    path('import/', views.ImportStudentsView.as_view(), name='student_import'),
    path('export/', views.ExportStudentsView.as_view(), name='student_export'),
    path('template/', views.DownloadTemplateView.as_view(), name='student_template'),
]
