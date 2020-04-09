from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.index, name='index'),
    path('apps', views.apps, name='apps'),
    path('app/<int:app_id>/', views.app, name='app'),
    path('releases', views.releases, name='releases'),
    path('release_input/', views.add_release, name='add_release'),
    path('release_input/<int:release_id>/', views.add_release, name='add_release'),
    path('ratings', views.ratings, name='ratings'),
    path('rating_input', views.add_ratings, name='add_ratings'),
]