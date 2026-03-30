from django import forms
from .models import ComplianceDocument


class ComplianceDocumentForm(forms.ModelForm):
    """
    Form for uploading a compliance document.
    We exclude `worker` because it is set automatically in the view
    (we always know which worker we're uploading for from the URL).
    """
    class Meta:
        model   = ComplianceDocument
        # Exclude `worker` — it's set in the view, not by the user
        exclude = ['worker']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
