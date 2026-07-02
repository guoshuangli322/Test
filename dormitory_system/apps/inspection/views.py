from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.db.models import Avg, Count
from .models import HygieneInspection
from .forms import InspectionForm


class AdminManagerMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_super_admin() or u.is_manager())


class InspectionListView(LoginRequiredMixin, ListView):
    model = HygieneInspection
    template_name = 'inspection/list.html'
    context_object_name = 'inspections'
    paginate_by = 20

    def get_queryset(self):
        qs = HygieneInspection.objects.select_related('room__building', 'inspector')
        kw = self.request.GET.get('keyword', '')
        grade = self.request.GET.get('grade', '')
        if kw:
            qs = qs.filter(room__room_number__icontains=kw)
        if grade:
            qs = qs.filter(grade=grade)
        # 学生只看自己房间
        if self.request.user.is_student():
            from apps.student_mgr.models import Student, DormitoryRecord
            try:
                s = Student.objects.get(user=self.request.user)
                bed = s.get_current_bed()
                if bed:
                    qs = qs.filter(room=bed.room)
                else:
                    qs = qs.none()
            except Student.DoesNotExist:
                qs = qs.none()
        return qs.order_by('-check_date')


class InspectionCreateView(AdminManagerMixin, CreateView):
    model = HygieneInspection
    form_class = InspectionForm
    template_name = 'inspection/form.html'
    success_url = reverse_lazy('inspection_list')

    def form_valid(self, form):
        form.instance.inspector = self.request.user
        messages.success(self.request, '检查记录添加成功')
        return super().form_valid(form)


class InspectionDetailView(LoginRequiredMixin, DetailView):
    model = HygieneInspection
    template_name = 'inspection/detail.html'
    context_object_name = 'inspection'


class InspectionStatisticsView(AdminManagerMixin, TemplateView):
    template_name = 'inspection/statistics.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total'] = HygieneInspection.objects.count()
        ctx['avg_score'] = HygieneInspection.objects.aggregate(Avg('score'))['score__avg'] or 0
        ctx['grade_stats'] = HygieneInspection.objects.values('grade').annotate(
            count=Count('id')).order_by('grade')
        return ctx
