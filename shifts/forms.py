from django import forms
from .models import Shift


class ShiftForm(forms.ModelForm):
    """
    Form for creating or editing a Shift.
    We add HTML5 date/time picker widgets so the browser
    renders a date-picker and time-picker instead of plain text inputs.
    """

    class Meta:
        model  = Shift
        fields = [
            'trust', 'role', 'department', 'nhs_band',
            'date', 'start_time', 'end_time', 'pay_rate',
            'required_skills', 'urgency', 'notes',
        ]
        widgets = {
            'date':       forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time'}),
            'notes':      forms.Textarea(attrs={'rows': 3}),
        }
