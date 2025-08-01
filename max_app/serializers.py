from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Annonce, Lieu, Favori, AlerteRecherche

# ---------------------
# Serializer Lieu
# ---------------------
class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = ['id', 'adresse', 'ville', 'code_postal', 'latitude', 'longitude']


# ---------------------
# Serializer Annonce (Lecture)
# ---------------------
class AnnonceSerializer(serializers.ModelSerializer):
    lieu = LieuSerializer(read_only=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Annonce
        fields = [
            'id', 'titre', 'description', 'prix', 'type_bien', 'surface',
            'nb_chambres', 'nb_salles_bain', 'lieu', 'date_creation',
            'nom_agent', 'telephone_agent', 'email_agent',
            'caracteristiques', 'images', 'distance'
        ]

    def get_distance(self, obj):
        # Distance calculée dynamiquement dans la vue
        return getattr(obj, 'distance', None)


# ---------------------
# Serializer Annonce (Création)
# ---------------------
class AnnonceCreateSerializer(serializers.ModelSerializer):
    # Champs supplémentaires pour créer un lieu
    adresse = serializers.CharField(write_only=True)
    ville = serializers.CharField(write_only=True)
    code_postal = serializers.CharField(write_only=True)
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Annonce
        fields = [
            'titre', 'description', 'prix', 'type_bien', 'surface',
            'nb_chambres', 'nb_salles_bain', 'nom_agent', 'telephone_agent',
            'email_agent', 'caracteristiques', 'images',
            'adresse', 'ville', 'code_postal', 'latitude', 'longitude'
        ]

    def create(self, validated_data):
        # Extraire les données du lieu
        lieu_data = {
            'adresse': validated_data.pop('adresse'),
            'ville': validated_data.pop('ville'),
            'code_postal': validated_data.pop('code_postal'),
            'latitude': validated_data.pop('latitude', None),
            'longitude': validated_data.pop('longitude', None),
        }

        # Créer le lieu
        lieu = Lieu.objects.create(**lieu_data)

        # Créer l'annonce
        annonce = Annonce.objects.create(lieu=lieu, **validated_data)
        return annonce


# ---------------------
# Serializer Favori
# ---------------------
class FavoriSerializer(serializers.ModelSerializer):
    annonce = AnnonceSerializer(read_only=True)
    annonce_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favori
        fields = ['id', 'annonce', 'annonce_id', 'date_ajout']
        read_only_fields = ['id', 'date_ajout']

    def create(self, validated_data):
        validated_data['utilisateur'] = self.context['request'].user
        return super().create(validated_data)


# ---------------------
# Serializer AlerteRecherche
# ---------------------
class AlerteRechercheSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlerteRecherche
        fields = [
            'id', 'nom', 'prix_min', 'prix_max', 'type_bien', 'ville',
            'surface_min', 'nb_chambres_min', 'nb_salles_bain_min',
            'mots_cles', 'latitude', 'longitude', 'rayon_km',
            'frequence', 'active', 'date_creation', 'derniere_notification'
        ]
        read_only_fields = ['id', 'date_creation', 'derniere_notification']

    def create(self, validated_data):
        validated_data['utilisateur'] = self.context['request'].user
        return super().create(validated_data)


# ---------------------
# Serializer User
# ---------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
