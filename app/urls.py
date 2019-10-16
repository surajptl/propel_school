from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('application', views.application),
    # path('snippet',views.snippet_detail)
]
