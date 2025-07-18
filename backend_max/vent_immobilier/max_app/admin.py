from django.contrib import admin
from .models import (
    Annonce, Bien, Caracteristique, Lieu, Media, Contact,
    TagSEO, SuggestionPrix, HistoriqueStatut
)

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_transaction', 'type_bien', 'statut', 'utilisateur', 'date_creation')
    list_filter = ('type_transaction', 'type_bien', 'statut', 'date_creation')
    search_fields = ('titre', 'description', 'nom_annonceur')

@admin.register(Bien)
class BienAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'superficie_totale', 'nombre_chambres', 'etat_general')
    search_fields = ('annonce__titre',)

@admin.register(Caracteristique)
class CaracteristiqueAdmin(admin.ModelAdmin):
    list_display = ('bien', 'type_caracteristique', 'actif')
    list_filter = ('type_caracteristique',)
    search_fields = ('bien__annonce__titre',)

@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'ville', 'pays')
    search_fields = ('ville', 'annonce__titre')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'type_media', 'ordre')
    list_filter = ('type_media',)
    search_fields = ('annonce__titre',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'nom', 'email', 'date_contact', 'lu')
    list_filter = ('lu', 'date_contact')
    search_fields = ('nom', 'email', 'annonce__titre')

@admin.register(TagSEO)
class TagSEOAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'mot_cle', 'poids')
    search_fields = ('mot_cle', 'annonce__titre')

@admin.register(SuggestionPrix)
class SuggestionPrixAdmin(admin.ModelAdmin):
    list_display = ('type_transaction', 'type_bien', 'ville', 'prix_moyen', 'date_creation')
    list_filter = ('type_transaction', 'type_bien', 'ville')
    search_fields = ('ville',)

@admin.register(HistoriqueStatut)
class HistoriqueStatutAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'ancien_statut', 'nouveau_statut', 'modifie_par', 'date_modification')
    list_filter = ('ancien_statut', 'nouveau_statut', 'date_modification')
    search_fields = ('annonce__titre', 'modifie_par__username')

# Register your models here.
