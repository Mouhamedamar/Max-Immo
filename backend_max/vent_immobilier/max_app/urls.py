from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnonceViewSet,
    BienViewSet,
    CaracteristiqueViewSet,
    LieuViewSet,
    MediaViewSet,
    ContactViewSet,
    TagSEOViewSet,
    SuggestionPrixViewSet,
    HistoriqueStatutViewSet,
)

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet, basename='annonce')
router.register(r'biens', BienViewSet, basename='bien')
router.register(r'caracteristiques', CaracteristiqueViewSet, basename='caracteristique')
router.register(r'lieux', LieuViewSet, basename='lieu')
router.register(r'medias', MediaViewSet, basename='media')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'tags-seo', TagSEOViewSet, basename='tagseo')
router.register(r'suggestions-prix', SuggestionPrixViewSet, basename='suggestionprix')
router.register(r'historiques-statut', HistoriqueStatutViewSet, basename='historiquestatut')

from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
]
