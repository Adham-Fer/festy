from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Ajoutez ces URLs si elles n'existent pas encore
    path('events/', views.events, name='events'),
    path('venues/', views.venues, name='venues'),
    path('organize/', views.organize, name='organize'),
    path('login/', views.login, name='login'),
]