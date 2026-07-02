from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView, View
from openpyxl import Workbook
from .models import OperationLog


class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_super_admin()


class LogListView(SuperAdminRequiredMixin, ListView):
    """操作日志列表"""
    model = OperationLog
    template_name = 'operation_log/list.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        qs = OperationLog.objects.all()
        kw = self.request.GET.get('keyword', '')
        module = self.request.GET.get('module', '')
        if kw:
            qs = qs.filter(username__icontains=kw) | qs.filter(action__icontains=kw)
        if module:
            qs = qs.filter(module=module)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['modules'] = OperationLog.objects.values_list('module', flat=True).distinct().order_by('module')
        return ctx


class ExportLogsView(SuperAdminRequiredMixin, View):
    """导出操作日志"""
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = '操作日志'
        ws.append(['用户名', '操作', '模块', 'IP地址', '请求方法', '请求路径', '详情', '操作时间'])
        for log in OperationLog.objects.all():
            ws.append([
                log.username, log.action, log.module, log.ip_address,
                log.request_method, log.request_path, log.detail,
                log.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=operation_logs.xlsx'
        wb.save(response)
        return response
