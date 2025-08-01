from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.conf import settings
import requests
from math import radians, cos, sin, asin, sqrt
import json

from .models import Lieu, Annonce, Favori, AlerteRecherche
from .serializers import (
    AnnonceSerializer, AnnonceCreateSerializer, FavoriSerializer,
    AlerteRechercheSerializer, LieuSerializer
)

# ---------------------------
# UTILITAIRE : GEOCODAGE (Google)
# ---------------------------
def geocoder_google(adresse):
    """Retourne latitude et longitude d'une adresse via Google Geocoding API"""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={adresse}&key={settings.GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None


@api_view(['GET', 'POST'])
def test_geocode(request):
    """Endpoint de test du geocoding via GET ou POST"""
    # Récupération adresse selon méthode
    if request.method == "GET":
        address = request.GET.get("address", "Dakar, Senegal")
    else:  # POST
        try:
            body = json.loads(request.body)
            address = body.get("address", "Dakar, Senegal")
        except json.JSONDecodeError:
            return Response({"error": "JSON invalide"}, status=status.HTTP_400_BAD_REQUEST)

    lat, lng = geocoder_google(address)
    if lat is None or lng is None:
        return Response({"error": "Adresse non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"adresse": address, "latitude": lat, "longitude": lng})


# ---------------------------
# UTILITAIRE : DISTANCE (Haversine)
# ---------------------------
def calcul_distance(lat1, lon1, lat2, lon2):
    """Calcule la distance entre deux points géographiques en km"""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c  # rayon moyen de la Terre en km


# ---------------------------
# PAGINATION STANDARD
# ---------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


# ---------------------------
# API LIEUX
# ---------------------------
class LieuListCreateView(generics.ListCreateAPIView):
    """API pour lister et créer des lieux"""
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer


# ---------------------------
# API ANNONCES
# ---------------------------
class AnnonceListCreateView(generics.ListCreateAPIView):
    queryset = Annonce.objects.filter(actif=True).select_related('lieu')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'lieu__ville', 'lieu__adresse']
    ordering_fields = ['prix', 'surface', 'date_creation']
    ordering = ['-date_creation']

    def get_serializer_class(self):
        return AnnonceCreateSerializer if self.request.method == 'POST' else AnnonceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        if params.get('prix_min'):
            queryset = queryset.filter(prix__gte=params['prix_min'])
        if params.get('prix_max'):
            queryset = queryset.filter(prix__lte=params['prix_max'])
        if params.get('type_bien'):
            queryset = queryset.filter(type_bien=params['type_bien'])
        if params.get('ville'):
            queryset = queryset.filter(lieu__ville__icontains=params['ville'])
        if params.get('surface_min'):
            queryset = queryset.filter(surface__gte=params['surface_min'])
        if params.get('nb_chambres'):
            queryset = queryset.filter(nb_chambres__gte=params['nb_chambres'])
        if params.get('nb_salles_bain'):
            queryset = queryset.filter(nb_salles_bain__gte=params['nb_salles_bain'])

        return queryset


class AnnonceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.filter(actif=True).select_related('lieu')
    serializer_class = AnnonceSerializer


# ---------------------------
# RECHERCHE PAR PROXIMITÉ
# ---------------------------
@api_view(['GET'])
def recherche_proximite(request):
    """
    Recherche d'annonces par géolocalisation avec rayon en utilisant Haversine
    GET /api/annonces/proximite/?lat=48.8566&lng=2.3522&rayon=10
    """
    try:
        latitude = float(request.GET.get('lat'))
        longitude = float(request.GET.get('lng'))
        rayon = float(request.GET.get('rayon', 10))
    except (TypeError, ValueError):
        return Response(
            {'error': 'Paramètres lat, lng et rayon requis et doivent être numériques'},
            status=status.HTTP_400_BAD_REQUEST
        )

    annonces = []
    for annonce in Annonce.objects.filter(actif=True).select_related('lieu'):
        if annonce.lieu and annonce.lieu.latitude and annonce.lieu.longitude:
            dist = calcul_distance(latitude, longitude, annonce.lieu.latitude, annonce.lieu.longitude)
            if dist <= rayon:
                annonces.append(annonce)

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(annonces, request)
    serializer = AnnonceSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


# ---------------------------
# API GEOCODER ADRESSE
# ---------------------------
@api_view(['POST'])
def geocoder_adresse(request):
    """Endpoint pour géocoder une adresse envoyée en POST"""
    adresse = request.data.get('adresse')
    if not adresse:
        return Response({'error': 'Adresse requise'}, status=status.HTTP_400_BAD_REQUEST)

    lat, lng = geocoder_google(adresse)
    if lat is None or lng is None:
        return Response({'error': 'Adresse non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'latitude': lat, 'longitude': lng, 'adresse': adresse})


# ---------------------------
# FAVORIS
# ---------------------------
class FavoriListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favori.objects.filter(utilisateur=self.request.user).select_related('annonce', 'annonce__lieu')


class FavoriDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favori.objects.filter(utilisateur=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favori(request, annonce_id):
    try:
        annonce = Annonce.objects.get(id=annonce_id, actif=True)
    except Annonce.DoesNotExist:
        return Response({'error': 'Annonce non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    favori, created = Favori.objects.get_or_create(utilisateur=request.user, annonce=annonce)
    if not created:
        favori.delete()
        return Response({'message': 'Annonce retirée des favoris', 'is_favorite': False})
    else:
        return Response({'message': 'Annonce ajoutée aux favoris', 'is_favorite': True})


# ---------------------------
# ALERTES DE RECHERCHE
# ---------------------------
class AlerteRechercheListCreateView(generics.ListCreateAPIView):
    serializer_class = AlerteRechercheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AlerteRecherche.objects.filter(utilisateur=self.request.user)


class AlerteRechercheDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlerteRechercheSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AlerteRecherche.objects.filter(utilisateur=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_alerte(request, alerte_id):
    try:
        alerte = AlerteRecherche.objects.get(id=alerte_id, utilisateur=request.user)
    except AlerteRecherche.DoesNotExist:
        return Response({'error': 'Alerte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    alerte.active = not alerte.active
    alerte.save()
    return Response({'message': f'Alerte {"activée" if alerte.active else "désactivée"}', 'active': alerte.active})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_alerte(request, alerte_id):
    try:
        alerte = AlerteRecherche.objects.get(id=alerte_id, utilisateur=request.user)
    except AlerteRecherche.DoesNotExist:
        return Response({'error': 'Alerte non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    queryset = Annonce.objects.filter(actif=True).select_related('lieu')

    # Filtres selon critères de l'alerte
    if alerte.prix_min:
        queryset = queryset.filter(prix__gte=alerte.prix_min)
    if alerte.prix_max:
        queryset = queryset.filter(prix__lte=alerte.prix_max)
    if alerte.type_bien:
        queryset = queryset.filter(type_bien=alerte.type_bien)
    if alerte.ville:
        queryset = queryset.filter(lieu__ville__icontains=alerte.ville)
    if alerte.surface_min:
        queryset = queryset.filter(surface__gte=alerte.surface_min)
    if alerte.nb_chambres_min:
        queryset = queryset.filter(nb_chambres__gte=alerte.nb_chambres_min)
    if alerte.nb_salles_bain_min:
        queryset = queryset.filter(nb_salles_bain__gte=alerte.nb_salles_bain_min)
    if alerte.mots_cles:
        queryset = queryset.filter(Q(titre__icontains=alerte.mots_cles) | Q(description__icontains=alerte.mots_cles))

    annonces_resultats = []
    if alerte.latitude and alerte.longitude and alerte.rayon_km:
        for annonce in queryset:
            if annonce.lieu and annonce.lieu.latitude and annonce.lieu.longitude:
                dist = calcul_distance(alerte.latitude, alerte.longitude, annonce.lieu.latitude, annonce.lieu.longitude)
                if dist <= alerte.rayon_km:
                    annonces_resultats.append(annonce)
    else:
        annonces_resultats = queryset

    serializer = AnnonceSerializer(annonces_resultats[:20], many=True)
    return Response({
        'alerte': AlerteRechercheSerializer(alerte).data,
        'nombre_resultats': len(annonces_resultats),
        'annonces_exemple': serializer.data
    })
