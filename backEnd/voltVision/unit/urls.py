from django.urls import path
from . import views

urlpatterns = [
    path('save-unit', views.create_Unit, name='create_unit'),
    path('unit-detail', views.unit_details, name='create_unit'),
]
