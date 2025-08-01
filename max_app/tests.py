from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.gis.geos import Point
from .models import Annonce, Lieu, Favori, AlerteRecherche


class AnnonceModelTest(TestCase):
    def setUp(self):
        self.lieu = Lieu.objects.create(
            adresse="123 Rue Test",
            ville="Paris",
            code_postal="75001",
            coordonnees=Point(2.3522, 48.8566)
        )
        
        self.annonce = Annonce.objects.create(
            titre="Appartement Test",
            description="Description test",
            prix=300000,
            type_bien="appartement",
            surface=75,
            nb_chambres=2,
            nb_salles_bain=1,
            lieu=self.lieu,
            nom_agent="Agent Test",
            telephone_agent="0123456789",
            email_agent="agent@test.com"
        )
    
    def test_annonce_creation(self):
        self.assertEqual(self.annonce.titre, "Appartement Test")
        self.assertEqual(self.annonce.lieu.ville, "Paris")
        self.assertTrue(self.annonce.actif)


class FavoriAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.lieu = Lieu.objects.create(
            adresse="123 Rue Test",
            ville="Paris",
            code_postal="75001"
        )
        
        self.annonce = Annonce.objects.create(
            titre="Appartement Test",
            description="Description test",
            prix=300000,
            type_bien="appartement",
            surface=75,
            lieu=self.lieu,
            nom_agent="Agent Test",
            telephone_agent="0123456789",
            email_agent="agent@test.com"
        )
    
    def test_add_favori(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('max_app:favori-list-create')
        data = {'annonce_id': self.annonce.id}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favori.objects.count(), 1)
    
    def test_list_favoris(self):
        Favori.objects.create(utilisateur=self.user, annonce=self.annonce)
        self.client.force_authenticate(user=self.user)
        
        url = reverse('max_app:favori-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_toggle_favori(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('max_app:toggle-favori', kwargs={'annonce_id': self.annonce.id})
        
        # Ajouter aux favoris
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_favorite'])
        self.assertEqual(Favori.objects.count(), 1)
        
        # Retirer des favoris
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_favorite'])
        self.assertEqual(Favori.objects.count(), 0)


class AlerteRechercheAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_alerte(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('max_app:alerte-list-create')
        data = {
            'nom': 'Alerte Test',
            'prix_max': 400000,
            'type_bien': 'appartement',
            'ville': 'Paris',
            'frequence': 'hebdomadaire'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AlerteRecherche.objects.count(), 1)
    
    def test_list_alertes(self):
        AlerteRecherche.objects.create(
            utilisateur=self.user,
            nom='Alerte Test',
            prix_max=400000
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('max_app:alerte-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class RechercheProximiteTest(APITestCase):
    def setUp(self):
        # Créer des lieux avec coordonnées
        self.lieu_paris = Lieu.objects.create(
            adresse="1 Rue de Rivoli",
            ville="Paris",
            code_postal="75001",
            coordonnees=Point(2.3522, 48.8566)  # Centre de Paris
        )
        
        self.lieu_banlieue = Lieu.objects.create(
            adresse="10 Avenue Test",
            ville="Boulogne",
            code_postal="92100",
            coordonnees=Point(2.2394, 48.8356)  # Boulogne-Billancourt
        )
        
        # Créer des annonces
        self.annonce_paris = Annonce.objects.create(
            titre="Appartement Paris Centre",
            description="Au coeur de Paris",
            prix=500000,
            type_bien="appartement",
            surface=60,
            lieu=self.lieu_paris,
            nom_agent="Agent Paris",
            telephone_agent="0123456789",
            email_agent="agent@paris.com"
        )
        
        self.annonce_banlieue = Annonce.objects.create(
            titre="Maison Banlieue",
            description="Proche de Paris",
            prix=400000,
            type_bien="maison",
            surface=100,
            lieu=self.lieu_banlieue,
            nom_agent="Agent Banlieue",
            telephone_agent="0123456789",
            email_agent="agent@banlieue.com"
        )
    
    def test_recherche_proximite(self):
        url = reverse('max_app:recherche-proximite')
        # Recherche autour du centre de Paris avec rayon de 10km
        response = self.client.get(url, {
            'lat': 48.8566,
            'lng': 2.3522,
            'rayon': 10
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Les deux annonces devraient être dans un rayon de 10km
        self.assertEqual(len(response.data['results']), 2)
    
    def test_recherche_proximite_rayon_reduit(self):
        url = reverse('max_app:recherche-proximite')
        # Recherche avec un rayon très petit (1km)
        response = self.client.get(url, {
            'lat': 48.8566,
            'lng': 2.3522,
            'rayon': 1
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Seule l'annonce de Paris devrait être dans un rayon de 1km
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['titre'], "Appartement Paris Centre")
