from django.contrib import admin
from .models import NHSTrust, Shift, Assignment


@admin.register(NHSTrust)
class NHSTrustAdmin(admin.ModelAdmin):
    list_display  = ['name', 'location', 'contact_email']
    search_fields = ['name', 'location']


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display  = ['role', 'trust', 'date', 'status', 'urgency', 'pay_rate']
    list_filter   = ['status', 'urgency', 'nhs_band']
    search_fields = ['role', 'department']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['worker', 'shift', 'status', 'match_score', 'assigned_at']
    list_filter  = ['status']
