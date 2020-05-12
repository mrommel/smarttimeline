from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.index, name='index'),
    path('apps/', views.apps, name='apps'),
    path('apps/<int:app_id>/', views.app, name='app'),
    path('releases/', views.releases, name='releases'),
    path('releases/add/', views.add_release, name='add_release'),
    path('releases/<int:release_id>/', views.add_release, name='add_release'),
    path('ratings/', views.ratings, name='ratings'),
    path('ratings/add/', views.add_ratings, name='add_ratings'),
]
