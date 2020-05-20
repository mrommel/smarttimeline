from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.index, name='index'),
    path('roadmap/<int:roadmap_id>/', views.roadmap, name='roadmap'),
]