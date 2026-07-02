from django import forms
from .models import UtilityBill


class UtilityBillForm(forms.ModelForm):
    class Meta:
        model = UtilityBill
        fields = ['building', 'room', 'year', 'month', 'utility_type',
                  'previous_reading', 'current_reading', 'unit_price', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'form-control'})
