# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Annonce(models.Model):
    TYPE_TRANSACTION = [
        ('vente', 'Vendre'),
        ('location', 'Louer'),
        ('location_saisonniere', 'Louer en saisonnier'),
    ]
    
    TYPE_BIEN = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
        ('bureau', 'Bureau'),
        ('villa', 'Villa'),
    ]
    
    ETAT_GENERAL = [
        ('neuf', 'Neuf'),
        ('bon', 'Bon'),
        ('a_renover', 'À rénover'),
    ]
    
    PROFIL_ANNONCEUR = [
        ('proprietaire', 'Propriétaire'),
        ('agence', 'Agence'),
        ('mandataire', 'Mandataire'),
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('suspendu', 'Suspendu'),
        ('expire', 'Expiré'),
    ]
    
    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    
    # Type d'annonce
    type_transaction = models.CharField(max_length=20, choices=TYPE_TRANSACTION)
    type_bien = models.CharField(max_length=20, choices=TYPE_BIEN)
    
    # Informations générales
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    devise = models.CharField(max_length=3, default='EUR')
    
    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    disponible_immediatement = models.BooleanField(default=True)
    
    # Timestamps
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_expiration = models.DateTimeField(null=True, blank=True)
    
    # Informations annonceur
    nom_annonceur = models.CharField(max_length=100)
    telephone_annonceur = models.CharField(max_length=20)
    email_annonceur = models.EmailField()
    profil_annonceur = models.CharField(max_length=20, choices=PROFIL_ANNONCEUR)
    affichage_public_coordonnees = models.BooleanField(default=False)
    
    # Métadonnées
    nombre_vues = models.PositiveIntegerField(default=0)
    nombre_contacts = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['type_transaction', 'type_bien']),
            models.Index(fields=['statut', 'date_creation']),
        ]
    
    def __str__(self):
        return f"{self.get_type_transaction_display()} - {self.get_type_bien_display()} - {self.titre}"


class Bien(models.Model):
    USAGE_TERRAIN = [
        ('habitation', 'Habitation'),
        ('commercial', 'Commercial'),
        ('agricole', 'Agricole'),
    ]
    
    annonce = models.OneToOneField(Annonce, on_delete=models.CASCADE, related_name='bien')
    
    # Caractéristiques générales
    superficie_habitable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    superficie_totale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Pour biens bâtis
    nombre_chambres = models.PositiveIntegerField(null=True, blank=True)
    nombre_salons = models.PositiveIntegerField(null=True, blank=True)
    nombre_salles_bain = models.PositiveIntegerField(null=True, blank=True)
    nombre_cuisines = models.PositiveIntegerField(null=True, blank=True)
    nombre_balcons = models.PositiveIntegerField(null=True, blank=True)
    etage = models.PositiveIntegerField(null=True, blank=True)
    annee_construction = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    
    # État
    etat_general = models.CharField(max_length=20, choices=Annonce.ETAT_GENERAL, null=True, blank=True)
    meuble = models.BooleanField(default=False)
    
    # Spécifique terrain
    terrain_titre = models.BooleanField(null=True, blank=True)
    viabilisation_eau = models.BooleanField(default=False)
    viabilisation_electricite = models.BooleanField(default=False)
    viabilisation_acces_route = models.BooleanField(default=False)
    usage_prevu = models.CharField(max_length=20, choices=USAGE_TERRAIN, null=True, blank=True)
    
    def __str__(self):
        return f"Bien - {self.annonce.titre}"


class Caracteristique(models.Model):
    TYPES_CARACTERISTIQUES = [
        ('piscine', 'Piscine'),
        ('jardin', 'Jardin'),
        ('terrasse', 'Terrasse'),
        ('parking', 'Parking'),
        ('securite_gardien', 'Gardien'),
        ('securite_alarme', 'Alarme'),
        ('securite_videosurveillance', 'Vidéosurveillance'),
        ('climatisation', 'Climatisation'),
        ('ascenseur', 'Ascenseur'),
        ('groupe_electrogene', 'Groupe électrogène'),
        ('internet_fibre', 'Internet/Fibre optique'),
        ('accessibilite_pmr', 'Accessibilité PMR'),
    ]
    
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, related_name='caracteristiques')
    type_caracteristique = models.CharField(max_length=30, choices=TYPES_CARACTERISTIQUES)
    actif = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['bien', 'type_caracteristique']
    
    def __str__(self):
        return f"{self.bien.annonce.titre} - {self.get_type_caracteristique_display()}"


class Lieu(models.Model):
    annonce = models.OneToOneField(Annonce, on_delete=models.CASCADE, related_name='lieu')
    
    # Adresse
    adresse_complete = models.TextField()
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=100, default='France')
    
    # Coordonnées GPS
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    def __str__(self):
        return f"{self.ville} - {self.annonce.titre}"


class Media(models.Model):
    TYPE_MEDIA = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]
    
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='medias')
    type_media = models.CharField(max_length=10, choices=TYPE_MEDIA)
    
    # Pour images
    fichier = models.ImageField(upload_to='annonces/images/', null=True, blank=True)
    
    # Pour vidéos
    lien_youtube = models.URLField(null=True, blank=True)
    fichier_video = models.FileField(upload_to='annonces/videos/', null=True, blank=True)
    
    # Métadonnées
    titre = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.annonce.titre} - {self.get_type_media_display()} {self.ordre}"


class Contact(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='contacts')
    
    # Informations contact
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, null=True, blank=True)
    
    # Message
    message = models.TextField()
    
    # Métadonnées
    date_contact = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_contact']
    
    def __str__(self):
        return f"Contact pour {self.annonce.titre} - {self.nom}"


# Modèle pour les tags SEO automatiques
class TagSEO(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='tags_seo')
    mot_cle = models.CharField(max_length=100)
    poids = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['annonce', 'mot_cle']
    
    def __str__(self):
        return f"{self.annonce.titre} - {self.mot_cle}"


# Modèle pour les suggestions de prix
class SuggestionPrix(models.Model):
    type_transaction = models.CharField(max_length=20, choices=Annonce.TYPE_TRANSACTION)
    type_bien = models.CharField(max_length=20, choices=Annonce.TYPE_BIEN)
    ville = models.CharField(max_length=100)
    prix_min = models.DecimalField(max_digits=12, decimal_places=2)
    prix_max = models.DecimalField(max_digits=12, decimal_places=2)
    prix_moyen = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Critères
    superficie_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    superficie_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Prix {self.type_transaction} {self.type_bien} - {self.ville}"

# Modèle pour l'historique des statuts d'annonce
from django.conf import settings

class HistoriqueStatut(models.Model):
    annonce = models.ForeignKey('Annonce', on_delete=models.CASCADE, related_name='historiques_statut')
    ancien_statut = models.CharField(max_length=20, choices=Annonce.STATUT_CHOICES)
    nouveau_statut = models.CharField(max_length=20, choices=Annonce.STATUT_CHOICES)
    modifie_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_modification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.annonce} : {self.ancien_statut} → {self.nouveau_statut} ({self.date_modification:%Y-%m-%d %H:%M})"