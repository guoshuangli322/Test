from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render
from .forms import UserCreateForm, UserEditForm
from .models import User

User = get_user_model()


def dashboard(request):
    """仪表盘首页 — 根据不同角色显示不同内容"""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('login')

    context = {}

    if request.user.is_super_admin():
        # 超级管理员：统计全局数据
        from apps.dorm.models import Building, Room, Bed
        from apps.student_mgr.models import Student
        from apps.repair.models import RepairOrder
        context.update({
            'building_count': Building.objects.count(),
            'room_count': Room.objects.count(),
            'bed_count': Bed.objects.count(),
            'student_count': Student.objects.filter(status='在校').count(),
            'pending_repair_count': RepairOrder.objects.filter(status='待处理').count(),
            'total_users': User.objects.count(),
        })
    elif request.user.is_manager():
        # 宿管：查看自己管理的楼栋
        from apps.dorm.models import Building
        from apps.repair.models import RepairOrder
        from apps.student_mgr.models import Student
        buildings = Building.objects.filter(manager=request.user)
        context.update({
            'buildings': buildings,
            'pending_repair_count': RepairOrder.objects.filter(status='待处理').count(),
            'student_count': Student.objects.filter(status='在校').count(),
        })
    elif request.user.is_student():
        # 学生：查看个人信息和宿舍信息
        from apps.student_mgr.models import Student, DormitoryRecord
        try:
            student = Student.objects.get(user=request.user)
            record = DormitoryRecord.objects.filter(student=student, status='入住中').first()
            context.update({
                'student': student,
                'current_record': record,
            })
        except Student.DoesNotExist:
            context['student'] = None

    return render(request, 'dashboard.html', context)


# ========== 用户管理 ==========

class SuperAdminRequiredMixin(UserPassesTestMixin):
    """超级管理员权限混入类"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_super_admin()


class UserListView(SuperAdminRequiredMixin, ListView):
    """用户列表"""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.GET.get('keyword', '')
        role = self.request.GET.get('role', '')
        if keyword:
            qs = qs.filter(username__icontains=keyword) | qs.filter(real_name__icontains=keyword)
        if role:
            qs = qs.filter(role=role)
        return qs


class UserCreateView(SuperAdminRequiredMixin, CreateView):
    """创建用户"""
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增用户'
        return context


class UserUpdateView(SuperAdminRequiredMixin, UpdateView):
    """编辑用户"""
    model = User
    form_class = UserEditForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑用户'
        return context


class UserDeleteView(SuperAdminRequiredMixin, DeleteView):
    """删除用户"""
    model = User
    success_url = reverse_lazy('user_list')

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'ok'})


class UserProfileView(LoginRequiredMixin, TemplateView):
    """个人中心"""
    template_name = 'accounts/profile.html'
