from django.urls import path

from allData import views

urlpatterns = [
    path('add', views.add, name='create'),
]
