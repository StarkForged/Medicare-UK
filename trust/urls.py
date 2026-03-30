from django.urls import path
from . import views
app_name = 'trust'
urlpatterns = [
    path('dashboard/', views.trust_dashboard, name='dashboard'),
    path('shifts/', views.trust_shifts, name='shifts'),
    path('approvals/', views.trust_approvals, name='approvals'),
    path('approvals/<int:pk>/approve/', views.approve_assignment, name='approve'),
    path('approvals/<int:pk>/reject/', views.reject_assignment, name='reject'),
]
