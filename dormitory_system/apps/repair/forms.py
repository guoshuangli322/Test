from django import forms
from .models import RepairOrder


class RepairOrderForm(forms.ModelForm):
    """学生提交报修"""
    class Meta:
        model = RepairOrder
        fields = ['title', 'category', 'building', 'room', 'description', 'contact_phone', 'images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})


class RepairProcessForm(forms.Form):
    """宿管/管理员处理报修"""
    status = forms.ChoiceField(label='处理状态', choices=[
        ('处理中', '处理中'), ('已完成', '已完成'), ('已关闭', '已关闭')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    assignee = forms.ModelChoiceField(
        queryset=None, label='指派人', required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    handler_note = forms.CharField(
        label='处理意见', required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def __init__(self, *args, **kwargs):
        from django.conf import settings
        super().__init__(*args, **kwargs)
        from apps.accounts.models import User
        self.fields['assignee'].queryset = User.objects.filter(is_active=True)
