from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_user, name='create'),
    path('get', views.get_user, name='user_detail'),
    path('get-all', views.get_all_users, name='get-all'),
]
