from django.contrib import admin
from django.urls import path, include
from .views import smbc_view

urlpatterns = [
    path('', smbc_view),
    path('<str:name>', smbc_view, name='comic'),
]
