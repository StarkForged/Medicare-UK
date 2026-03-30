from django.contrib import admin
from .models import ComplianceDocument


@admin.register(ComplianceDocument)
class ComplianceDocumentAdmin(admin.ModelAdmin):
    list_display   = ['title', 'worker', 'doc_type', 'expiry_date', 'status']
    list_filter    = ['status', 'doc_type']
    search_fields  = ['title', 'worker__first_name', 'worker__last_name']
    readonly_fields = ['created_at']
