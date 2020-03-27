from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.index, name='index'),
    path('releases', views.releases, name='releases'),
    path('ratings', views.ratings, name='ratings'),
    path('rating_input', views.add_ratings, name='add_ratings'),
]