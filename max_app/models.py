from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Lieu(models.Model):
    ville = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10, null=True, blank=True)  # AJOUT
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.adresse}, {self.ville}"

    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"


class Annonce(models.Model):
    TYPE_BIEN_CHOICES = [
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
        ('commercial', 'Commercial'),
        ('terrain', 'Terrain'),
    ]
    
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    type_bien = models.CharField(max_length=20, choices=TYPE_BIEN_CHOICES)
    surface = models.FloatField(validators=[MinValueValidator(0)])
    nb_chambres = models.PositiveIntegerField(null=True, blank=True)
    nb_salles_bain = models.PositiveIntegerField(null=True, blank=True)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE, related_name='annonces')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
    
    # Informations agent
    nom_agent = models.CharField(max_length=100)
    telephone_agent = models.CharField(max_length=20)
    email_agent = models.EmailField()
    
    # Caractéristiques supplémentaires
    caracteristiques = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"


class Favori(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='favoris')
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('utilisateur', 'annonce')
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        ordering = ['-date_ajout']
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.annonce.titre}"


class AlerteRecherche(models.Model):
    FREQUENCE_CHOICES = [
        ('quotidienne', 'Quotidienne'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertes')
    nom = models.CharField(max_length=100)
    
    prix_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prix_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    type_bien = models.CharField(max_length=20, choices=Annonce.TYPE_BIEN_CHOICES, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    surface_min = models.FloatField(null=True, blank=True)
    nb_chambres_min = models.PositiveIntegerField(null=True, blank=True)
    nb_salles_bain_min = models.PositiveIntegerField(null=True, blank=True)
    mots_cles = models.CharField(max_length=255, blank=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rayon_km = models.PositiveIntegerField(null=True, blank=True, help_text="Rayon en kilomètres")
    
    frequence = models.CharField(max_length=20, choices=FREQUENCE_CHOICES, default='hebdomadaire')
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_notification = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Alerte de recherche"
        verbose_name_plural = "Alertes de recherche"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.nom}"
