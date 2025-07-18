from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly

from .models import (
    Annonce, Bien, Caracteristique, Lieu,
    Media, Contact, TagSEO, SuggestionPrix
)

from .serializers import (
    AnnonceSerializer, BienSerializer, CaracteristiqueSerializer, LieuSerializer,
    MediaSerializer, ContactSerializer, TagSEOSerializer, SuggestionPrixSerializer,
    HistoriqueStatutSerializer
)
from .models import HistoriqueStatut

# --------------------- ANNONCE ---------------------

class AnnonceViewSet(viewsets.ModelViewSet):
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type_bien', 'type_transaction', 'statut', 'lieu__ville', 'prix']
    search_fields = ['titre', 'type_bien', 'type_transaction', 'nom_annonceur']
    ordering_fields = ['prix', 'date_creation', 'nombre_vues']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Annonce.objects.all()
        elif user.is_authenticated:
            return Annonce.objects.filter(utilisateur=user)
        return Annonce.objects.filter(statut='publie')

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=['get'], url_path='medias')
    def get_medias(self, request, pk=None):
        annonce = self.get_object()
        medias = annonce.medias.all()
        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='historique-statut')
    def historique_statut(self, request, pk=None):
        annonce = self.get_object()
        historiques = HistoriqueStatut.objects.filter(annonce=annonce).order_by('-date_modification')
        serializer = HistoriqueStatutSerializer(historiques, many=True)
        return Response(serializer.data)

# --------------------- BIEN ---------------------

class BienViewSet(viewsets.ModelViewSet):
    queryset = Bien.objects.all()
    serializer_class = BienSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- CARACTÉRISTIQUE ---------------------

class CaracteristiqueViewSet(viewsets.ModelViewSet):
    queryset = Caracteristique.objects.all()
    serializer_class = CaracteristiqueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- LIEU ---------------------

class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- MEDIA ---------------------

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- CONTACT ---------------------

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

# --------------------- TAG SEO ---------------------

class TagSEOViewSet(viewsets.ModelViewSet):
    queryset = TagSEO.objects.all()
    serializer_class = TagSEOSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- SUGGESTION PRIX ---------------------

class SuggestionPrixViewSet(viewsets.ModelViewSet):
    queryset = SuggestionPrix.objects.all()
    serializer_class = SuggestionPrixSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --------------------- HISTORIQUE STATUT ---------------------

class HistoriqueStatutViewSet(viewsets.ModelViewSet):
    queryset = HistoriqueStatut.objects.all()
    serializer_class = HistoriqueStatutSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
