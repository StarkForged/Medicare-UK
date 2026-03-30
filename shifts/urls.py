from django.urls import path
from . import views

app_name = 'shifts'

urlpatterns = [
    path('',                              views.shift_list,    name='list'),
    path('create/',                       views.shift_create,  name='create'),
    path('<int:pk>/',                     views.shift_detail,  name='detail'),
    path('<int:shift_pk>/assign/',        views.assign_worker, name='assign'),
    path('assignments/',                  views.assignment_list, name='assignments'),
]
