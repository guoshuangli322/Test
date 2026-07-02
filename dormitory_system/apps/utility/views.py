from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, View
from openpyxl import Workbook
from .models import UtilityBill
from .forms import UtilityBillForm


class AdminManagerMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_super_admin() or u.is_manager())


class UtilityBillListView(LoginRequiredMixin, ListView):
    """水电账单列表"""
    model = UtilityBill
    template_name = 'utility/list.html'
    context_object_name = 'bills'
    paginate_by = 20

    def get_queryset(self):
        qs = UtilityBill.objects.select_related('room__building')
        # 学生只看自己房间的账单
        if self.request.user.is_student():
            from apps.student_mgr.models import Student
            try:
                student = Student.objects.get(user=self.request.user)
                bed = student.get_current_bed()
                if bed:
                    qs = qs.filter(room=bed.room)
                else:
                    qs = qs.none()
            except Student.DoesNotExist:
                qs = qs.none()
        # 筛选
        kw = self.request.GET.get('keyword', '')
        status = self.request.GET.get('status', '')
        month = self.request.GET.get('month', '')
        if kw:
            qs = qs.filter(room__room_number__icontains=kw)
        if status:
            qs = qs.filter(status=status)
        if month:
            y, m = month.split('-')
            qs = qs.filter(year=int(y), month=int(m))
        return qs.order_by('-year', '-month', 'room__room_number')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # 获取所有可用的月份，用于筛选
        months = UtilityBill.objects.values_list('year', 'month').distinct().order_by('-year', '-month')
        ctx['month_list'] = [(f'{y}-{m:02d}', f'{y}年{m}月') for y, m in months]
        ctx['STATUS_CHOICES'] = ['未缴纳', '已缴纳', '已减免']
        return ctx


class UtilityBillCreateView(AdminManagerMixin, CreateView):
    model = UtilityBill
    form_class = UtilityBillForm
    template_name = 'utility/form.html'
    success_url = reverse_lazy('utility_list')

    def form_valid(self, form):
        messages.success(self.request, '账单添加成功')
        return super().form_valid(form)


class UtilityBillUpdateView(AdminManagerMixin, UpdateView):
    model = UtilityBill
    form_class = UtilityBillForm
    template_name = 'utility/form.html'
    success_url = reverse_lazy('utility_list')

    def form_valid(self, form):
        messages.success(self.request, '账单已更新')
        return super().form_valid(form)


class UtilityBillPayView(LoginRequiredMixin, View):
    """缴纳账单"""
    def post(self, request, pk):
        bill = get_object_or_404(UtilityBill, pk=pk)
        bill.status = '已缴纳'
        bill.save()
        messages.success(request, f'{bill} 缴纳成功')
        return redirect('utility_list')


class ExportUtilityView(AdminManagerMixin, View):
    """导出水电账单"""
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = '水电账单'
        ws.append(['楼栋', '房间', '年份', '月份', '类型', '上次读数', '本次读数', '用量', '单价', '金额', '状态'])
        bills = UtilityBill.objects.select_related('room__building').all()
        for b in bills:
            ws.append([
                b.building.name, b.room.room_number, b.year, b.month,
                b.get_utility_type_display(), float(b.previous_reading),
                float(b.current_reading), float(b.usage), float(b.unit_price),
                float(b.amount), b.status
            ])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=utility_bills.xlsx'
        wb.save(response)
        return response
