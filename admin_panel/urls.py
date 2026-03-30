from django.urls import path
from . import views
app_name = 'admin_panel'
urlpatterns = [
    path('overview/', views.platform_overview, name='overview'),
    path('users/', views.user_management, name='users'),
    path('trusts/', views.trust_management, name='trusts'),
]
