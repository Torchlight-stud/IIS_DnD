from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('new_session/', views.new_session, name='new_session'),
    path('', views.home, name='home')
]