from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import RepairOrder, RepairCategory
from .forms import RepairOrderForm, RepairProcessForm
from django.utils import timezone


class RepairListView(LoginRequiredMixin, ListView):
    """报修列表"""
    model = RepairOrder
    template_name = 'repair/list.html'
    context_object_name = 'repairs'
    paginate_by = 15

    def get_queryset(self):
        qs = RepairOrder.objects.select_related('category', 'building', 'reporter')
        if self.request.user.is_student():
            qs = qs.filter(reporter=self.request.user)
        kw = self.request.GET.get('keyword', '')
        status = self.request.GET.get('status', '')
        if kw:
            qs = qs.filter(title__icontains=kw) | qs.filter(order_no__icontains=kw)
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')


class MyRepairView(LoginRequiredMixin, ListView):
    """我的报修（学生视角）"""
    model = RepairOrder
    template_name = 'repair/my_repairs.html'
    context_object_name = 'repairs'
    paginate_by = 15

    def get_queryset(self):
        return RepairOrder.objects.filter(reporter=self.request.user).order_by('-created_at')


class RepairCreateView(LoginRequiredMixin, CreateView):
    """提交报修"""
    model = RepairOrder
    form_class = RepairOrderForm
    template_name = 'repair/create.html'
    success_url = reverse_lazy('my_repairs')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, '报修提交成功')
        return super().form_valid(form)


class RepairDetailView(LoginRequiredMixin, DetailView):
    """报修详情"""
    model = RepairOrder
    template_name = 'repair/detail.html'
    context_object_name = 'repair'


class RepairProcessView(LoginRequiredMixin, UpdateView):
    """处理报修（宿管/管理员）"""
    model = RepairOrder
    template_name = 'repair/process.html'
    form_class = RepairOrderForm

    def get_form_class(self):
        return RepairProcessForm

    def get_success_url(self):
        return reverse_lazy('repair_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.status = form.cleaned_data['status']
        self.object.assignee = form.cleaned_data.get('assignee')
        self.object.handler_note = form.cleaned_data.get('handler_note', '')
        if self.object.status == '已完成':
            self.object.completed_at = timezone.now()
        self.object.save()
        messages.success(self.request, '工单处理成功')
        return redirect(self.get_success_url())
