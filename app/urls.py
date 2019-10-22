
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('application/', views.application, name='application'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/application/', views.edit_application, name='edit_application'),
]
