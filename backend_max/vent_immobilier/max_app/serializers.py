from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Annonce, Bien, Caracteristique, Lieu, Media,
    Contact, TagSEO, SuggestionPrix
)
try:
    from .models import HistoriqueStatut
except ImportError:
    HistoriqueStatut = None

# -------------------- UTILISATEUR --------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# -------------------- MODELES SIMPLES --------------------

class CaracteristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristique
        fields = '__all__'

class TagSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagSEO
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class SuggestionPrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionPrix
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

# -------------------- MODELES IMBRIQUÉS --------------------

class BienSerializer(serializers.ModelSerializer):
    caracteristiques = CaracteristiqueSerializer(many=True, read_only=True)

    class Meta:
        model = Bien
        fields = '__all__'

class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = '__all__'

# -------------------- ANNONCE PRINCIPALE --------------------

# -------------------- HISTORIQUE STATUT --------------------

class HistoriqueStatutSerializer(serializers.ModelSerializer):
    modifie_par = UserSerializer(read_only=True)
    ancien_statut_label = serializers.SerializerMethodField()
    nouveau_statut_label = serializers.SerializerMethodField()

    class Meta:
        model = HistoriqueStatut
        fields = [
            'id', 'annonce', 'ancien_statut', 'ancien_statut_label',
            'nouveau_statut', 'nouveau_statut_label',
            'modifie_par', 'date_modification'
        ]

    def get_ancien_statut_label(self, obj):
        return dict(Annonce.STATUT_CHOICES).get(obj.ancien_statut)

    def get_nouveau_statut_label(self, obj):
        return dict(Annonce.STATUT_CHOICES).get(obj.nouveau_statut)

class AnnonceSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    bien = BienSerializer(read_only=True)
    lieu = LieuSerializer(read_only=True)
    medias = MediaSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    tags_seo = TagSEOSerializer(many=True, read_only=True)

    class Meta:
        model = Annonce
        fields = '__all__'
        read_only_fields = [
            'id', 'utilisateur', 'date_creation', 'date_modification',
            'nombre_vues', 'nombre_contacts'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['utilisateur'] = request.user
        return super().create(validated_data)

    def validate(self, data):
        if data.get('prix') is not None and data['prix'] <= 0:
            raise serializers.ValidationError({"prix": "Le prix doit être supérieur à zéro."})
        return data
