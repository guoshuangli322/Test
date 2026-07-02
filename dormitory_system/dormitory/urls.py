from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.accounts import views as accounts_views

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),

    # 首页/仪表盘
    path('', accounts_views.dashboard, name='dashboard'),

    # 账户模块
    path('accounts/', include('apps.accounts.urls')),

    # 宿舍管理
    path('dorm/', include('apps.dorm.urls')),

    # 学生管理
    path('students/', include('apps.student_mgr.urls')),

    # 报修管理
    path('repair/', include('apps.repair.urls')),

    # 水电账单
    path('utility/', include('apps.utility.urls')),

    # 卫生检查
    path('inspection/', include('apps.inspection.urls')),

    # 公告管理
    path('announcement/', include('apps.announcement.urls')),

    # 操作日志
    path('logs/', include('apps.operation_log.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
