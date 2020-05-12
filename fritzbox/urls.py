from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.index, name='index'),
    path('check/<int:box_config_id>/', views.check, name='check'),
    path('wifi/<int:box_config_id>/', views.wifi, name='wifi'),
    path('hosts/<int:box_config_id>/', views.hosts, name='hosts'),
    path('status/<int:box_config_id>/', views.status, name='status'),
]