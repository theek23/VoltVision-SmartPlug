from django.urls import path
from . import views

urlpatterns = [
    path('add', views.create_Unit, name='create'),
    path('unit-detail', views.unit_details, name='unit_detail'),
    path('get-all', views.get_All_unit, name='get_all'),
    path('search-unit', views.search_unit, name='search_unit'),
    path('last-id', views.get_last_unit_id, name='last_id'),
    path('exm', views.ex, name='ex'),
]
