from django import forms
from .models import Worker


class WorkerForm(forms.ModelForm):
    """
    Form for adding or editing a Worker.
    We exclude `agency` because it is always set to the logged-in user
    in the view — we never want the form to expose it.
    """
    class Meta:
        model   = Worker
        exclude = ['agency', 'status', 'rating', 'shifts_completed']
        widgets = {
            'skills': forms.TextInput(attrs={
                'placeholder': 'e.g. ICU, ACLS, Ventilator, Chest Drains'
            }),
        }
