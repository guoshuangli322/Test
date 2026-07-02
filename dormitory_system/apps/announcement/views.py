from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Announcement
from .forms import AnnouncementForm


class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcement/list.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_queryset(self):
        qs = Announcement.objects.filter(is_active=True)
        kw = self.request.GET.get('keyword', '')
        cat = self.request.GET.get('category', '')
        if kw:
            qs = qs.filter(title__icontains=kw)
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pinned'] = Announcement.objects.filter(is_active=True, is_pinned=True)
        return ctx


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement/form.html'
    success_url = reverse_lazy('announcement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '公告发布成功')
        return super().form_valid(form)


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'announcement/detail.html'
    context_object_name = 'announcement'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Announcement.objects.filter(pk=obj.pk).update(views=models.F('views') + 1)
        obj.views += 1
        return obj


from django.db import models as models


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcement/form.html'
    success_url = reverse_lazy('announcement_list')

    def get_success_url(self):
        return reverse_lazy('announcement_detail', kwargs={'pk': self.object.pk})


class AnnouncementDeleteView(LoginRequiredMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcement_list')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
