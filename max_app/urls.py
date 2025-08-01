from django.urls import path
from .views import (
    # Lieux
    LieuListCreateView,

    # Annonces
    AnnonceListCreateView, AnnonceDetailView, recherche_proximite,

    # Géocodage
    test_geocode, geocoder_adresse,

    # Favoris
    FavoriListCreateView, FavoriDetailView, toggle_favori,

    # Alertes
    AlerteRechercheListCreateView, AlerteRechercheDetailView,
    toggle_alerte, test_alerte
)

urlpatterns = [
    # -------------------
    # API Lieux
    # -------------------
    path('lieux/', LieuListCreateView.as_view(), name='lieu-list-create'),

    # -------------------
    # API Annonces
    # -------------------
    path('annonces/proximite/', recherche_proximite, name='annonce-proximite'),  # placer avant <pk>
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce-list-create'),
    path('annonces/<int:pk>/', AnnonceDetailView.as_view(), name='annonce-detail'),

    # -------------------
    # API Géocodage
    # -------------------
    path('test-geocode/', test_geocode, name='test-geocode'),   # Endpoint de test (GET/POST)
    path('geocoder/', geocoder_adresse, name='geocoder-adresse'),  # Endpoint officiel (POST)

    # -------------------
    # API Favoris
    # -------------------
    path('favoris/toggle/<int:annonce_id>/', toggle_favori, name='favori-toggle'),  # avant <pk>
    path('favoris/', FavoriListCreateView.as_view(), name='favori-list-create'),
    path('favoris/<int:pk>/', FavoriDetailView.as_view(), name='favori-detail'),

    # -------------------
    # API Alertes
    # -------------------
    path('alertes/toggle/<int:alerte_id>/', toggle_alerte, name='alerte-toggle'),
    path('alertes/test/<int:alerte_id>/', test_alerte, name='alerte-test'),
    path('alertes/', AlerteRechercheListCreateView.as_view(), name='alerte-list-create'),
    path('alertes/<int:pk>/', AlerteRechercheDetailView.as_view(), name='alerte-detail'),
]
