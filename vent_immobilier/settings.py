import os
from pathlib import Path
from decouple import config

# ---------------------------
# BASE DIR
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# CLÉS ET DEBUG
# ---------------------------
SECRET_KEY = 'remplace-moi-par-ta-clé-secrète'
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ---------------------------
# APPLICATIONS INSTALLÉES
# ---------------------------
INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # API REST
    'rest_framework',
    'django_filters',
    'corsheaders',
    'rest_framework.authtoken',

    # Application principale
    'max_app',
]

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS en premier
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URLS ET WSGI
# ---------------------------
ROOT_URLCONF = 'vent_immobilier.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Dossier templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vent_immobilier.wsgi.application'

# ---------------------------
# BASE DE DONNÉES
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Change si tu veux PostgreSQL
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# VALIDATEURS DE MOTS DE PASSE
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ---------------------------
# LANGUE ET TEMPS
# ---------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# FICHIERS STATIQUES & MEDIA
# ---------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Créer le dossier static s’il n’existe pas
os.makedirs(BASE_DIR / "static", exist_ok=True)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# CONFIGURATION REST FRAMEWORK
# ---------------------------
REST_FRAMEWORK = {
    # Authentification par token
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # Permissions par défaut
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Filtres et pagination
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ---------------------------
# CONFIGURATION CORS
# ---------------------------
CORS_ALLOW_ALL_ORIGINS = True
# En production, mieux de limiter :
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# ---------------------------
# GOOGLE MAPS API
# ---------------------------
from decouple import config

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')

