from django.contrib import admin
from .models import Lieu, Annonce, Favori, AlerteRecherche

@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ['adresse', 'ville', 'latitude', 'longitude']
    list_filter = ['ville']
    search_fields = ['adresse', 'ville']


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'prix', 'type_bien', 'surface', 'lieu', 'date_creation', 'actif']
    list_filter = ['type_bien', 'actif', 'date_creation', 'lieu__ville']
    search_fields = ['titre', 'description', 'lieu__ville', 'lieu__adresse']
    readonly_fields = ['date_creation', 'date_modification']
    list_editable = ['actif']

    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'prix', 'type_bien', 'actif')
        }),
        ('Caractéristiques', {
            'fields': ('surface', 'nb_chambres', 'nb_salles_bain', 'caracteristiques')
        }),
        ('Localisation', {
            'fields': ('lieu',)
        }),
        ('Agent', {
            'fields': ('nom_agent', 'telephone_agent', 'email_agent')
        }),
        ('Médias', {
            'fields': ('images',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'annonce', 'date_ajout']
    list_filter = ['date_ajout']
    search_fields = ['utilisateur__username', 'annonce__titre']
    readonly_fields = ['date_ajout']


@admin.register(AlerteRecherche)
class AlerteRechercheAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'nom', 'frequence', 'active', 'date_creation']
    list_filter = ['frequence', 'active', 'type_bien', 'date_creation']
    search_fields = ['utilisateur__username', 'nom', 'ville', 'mots_cles']
    readonly_fields = ['date_creation', 'derniere_notification']
    list_editable = ['active']

    fieldsets = (
        ('Informations générales', {
            'fields': ('utilisateur', 'nom', 'active', 'frequence')
        }),
        ('Critères de prix', {
            'fields': ('prix_min', 'prix_max')
        }),
        ('Critères de bien', {
            'fields': ('type_bien', 'surface_min', 'nb_chambres_min', 'nb_salles_bain_min')
        }),
        ('Localisation', {
            'fields': ('ville', 'latitude', 'longitude', 'rayon_km')
        }),
        ('Recherche textuelle', {
            'fields': ('mots_cles',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'derniere_notification'),
            'classes': ('collapse',)
        }),
    )
