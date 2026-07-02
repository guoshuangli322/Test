from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    """学生信息表单"""
    class Meta:
        model = Student
        fields = ['student_id', 'real_name', 'gender', 'class_name', 'college',
                  'phone', 'parent_phone', 'enroll_date', 'remark']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})
