from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from .models import Building, Room, Bed
from .forms import BuildingForm, RoomForm, BedForm


class AdminOrManagerMixin(UserPassesTestMixin):
    """管理员或宿管权限"""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_super_admin() or user.is_manager())


# ===== 楼栋管理 =====

class BuildingListView(AdminOrManagerMixin, ListView):
    model = Building
    template_name = 'dorm/building_list.html'
    context_object_name = 'buildings'
    paginate_by = 10

    def get_queryset(self):
        qs = Building.objects.all()
        if self.request.user.is_manager():
            qs = qs.filter(manager=self.request.user)
        kw = self.request.GET.get('keyword', '')
        if kw:
            qs = qs.filter(name__icontains=kw) | qs.filter(code__icontains=kw)
        return qs


class BuildingCreateView(AdminOrManagerMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'dorm/building_form.html'
    success_url = reverse_lazy('building_list')

    def form_valid(self, form):
        messages.success(self.request, '楼栋添加成功')
        return super().form_valid(form)


class BuildingUpdateView(AdminOrManagerMixin, UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'dorm/building_form.html'
    success_url = reverse_lazy('building_list')

    def form_valid(self, form):
        messages.success(self.request, '楼栋信息已更新')
        return super().form_valid(form)


class BuildingDeleteView(AdminOrManagerMixin, DeleteView):
    model = Building
    success_url = reverse_lazy('building_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '楼栋已删除')
        return super().delete(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# ===== 房间管理 =====

class RoomListView(AdminOrManagerMixin, ListView):
    model = Room
    template_name = 'dorm/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 20

    def get_queryset(self):
        building_id = self.kwargs.get('pk')
        qs = Room.objects.filter(building_id=building_id)
        floor = self.request.GET.get('floor', '')
        if floor:
            qs = qs.filter(floor=floor)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['building'] = get_object_or_404(Building, pk=self.kwargs['pk'])
        return ctx


class RoomCreateView(AdminOrManagerMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'dorm/room_form.html'

    def get_success_url(self):
        return reverse_lazy('room_list', kwargs={'pk': self.object.building_id})

    def form_valid(self, form):
        messages.success(self.request, '房间添加成功')
        return super().form_valid(form)

    def get_initial(self):
        building_id = self.request.GET.get('building')
        if building_id:
            return {'building': building_id}
        return {}


class RoomUpdateView(AdminOrManagerMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'dorm/room_form.html'

    def get_success_url(self):
        return reverse_lazy('room_list', kwargs={'pk': self.object.building_id})


class RoomDeleteView(AdminOrManagerMixin, DeleteView):
    model = Room

    def get_success_url(self):
        return reverse_lazy('room_list', kwargs={'pk': self.object.building_id})

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# ===== 床位管理 =====

class BedListView(AdminOrManagerMixin, ListView):
    model = Bed
    template_name = 'dorm/bed_list.html'
    context_object_name = 'beds'
    paginate_by = 30

    def get_queryset(self):
        room_id = self.kwargs.get('pk')
        return Bed.objects.filter(room_id=room_id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['room'] = get_object_or_404(Room, pk=self.kwargs['pk'])
        return ctx


class BedCreateView(AdminOrManagerMixin, CreateView):
    model = Bed
    form_class = BedForm
    template_name = 'dorm/bed_form.html'

    def get_success_url(self):
        return reverse_lazy('bed_list', kwargs={'pk': self.object.room_id})

    def get_initial(self):
        room_id = self.request.GET.get('room')
        if room_id:
            return {'room': room_id}
        return {}


class BedUpdateView(AdminOrManagerMixin, UpdateView):
    model = Bed
    form_class = BedForm
    template_name = 'dorm/bed_form.html'

    def get_success_url(self):
        return reverse_lazy('bed_list', kwargs={'pk': self.object.room_id})


class BedDeleteView(AdminOrManagerMixin, DeleteView):
    model = Bed

    def get_success_url(self):
        return reverse_lazy('bed_list', kwargs={'pk': self.object.room_id})

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# ===== 批量生成 =====

class BatchCreateView(AdminOrManagerMixin, TemplateView):
    """批量生成房间和床位"""
    template_name = 'dorm/batch_create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buildings'] = Building.objects.filter(is_active=True)
        return ctx

    def post(self, request, *args, **kwargs):
        building_id = request.POST.get('building')
        start_floor = int(request.POST.get('start_floor', 1))
        end_floor = int(request.POST.get('end_floor', 6))
        rooms_per_floor = int(request.POST.get('rooms_per_floor', 10))
        bed_count = int(request.POST.get('bed_count', 4))
        room_type = request.POST.get('room_type', '四人寝')
        start_num = int(request.POST.get('start_num', 1))

        building = get_object_or_404(Building, pk=building_id)
        created = 0
        for floor in range(start_floor, end_floor + 1):
            for i in range(rooms_per_floor):
                num = start_num + i
                room_number = f'{floor:02d}{num:02d}'
                room, ok = Room.objects.get_or_create(
                    building=building,
                    room_number=room_number,
                    defaults={
                        'room_type': room_type,
                        'bed_count': bed_count,
                        'floor': floor,
                    }
                )
                if ok:
                    # 自动生成床位
                    for b in range(1, bed_count + 1):
                        Bed.objects.get_or_create(
                            room=room,
                            bed_number=f'{b}号床'
                        )
                    created += 1

        messages.success(request, f'批量创建完成，共生成 {created} 间房间')
        return redirect('building_list')
