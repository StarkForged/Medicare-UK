from django.urls import path
from django.shortcuts import redirect
from . import views
app_name = 'core'
urlpatterns = [
    path('', lambda req: redirect('core:dashboard'), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
