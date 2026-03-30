from django.urls import path
from . import views
app_name = 'workers'
urlpatterns = [
    path('', views.worker_list, name='list'),
    path('add/', views.worker_add, name='add'),
    path('<int:pk>/', views.worker_detail, name='detail'),
    path('<int:pk>/edit/', views.worker_edit, name='edit'),
]
