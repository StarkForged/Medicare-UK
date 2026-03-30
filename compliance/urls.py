from django.urls import path
from . import views
app_name = 'compliance'
urlpatterns = [
    path('', views.compliance_overview, name='overview'),
    path('workers/<int:worker_pk>/add-doc/', views.document_add, name='document_add'),
]
