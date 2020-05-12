from django.urls import path

from . import views

urlpatterns = [
    path('content/<int:content_id>/', views.content, name='content'),
]