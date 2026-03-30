from django.contrib import admin
from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display   = ['get_full_name', 'role', 'nhs_band', 'status', 'nmc_pin', 'shifts_completed']
    list_filter    = ['nhs_band', 'status', 'right_to_work']
    search_fields  = ['first_name', 'last_name', 'nmc_pin', 'email']
    readonly_fields = ['created_at', 'updated_at']
