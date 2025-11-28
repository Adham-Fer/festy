from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_evenements, name='liste_evenements'),
    path('ajouter/', views.ajouter_evenement, name='ajouter_evenement'),
    path('<int:pk>/', views.detail_evenement, name='detail_evenement'),
]
