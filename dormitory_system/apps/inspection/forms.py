from django import forms
from .models import HygieneInspection


class InspectionForm(forms.ModelForm):
    class Meta:
        model = HygieneInspection
        fields = ['building', 'room', 'score', 'comment', 'images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if not isinstance(f.widget, forms.FileInput):
                f.widget.attrs.update({'class': 'form-control'})
