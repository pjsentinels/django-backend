from pathlib import Path
import os

from backend.vault import get_secret, is_ci

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Obtenemos el secreto una sola vez para optimizar
vault_data = get_secret("myapp/django")

# =========================
# SECRET KEY
# =========================
# Si hay datos en Vault los usa, si no, usa la clave de desarrollo
SECRET_KEY = vault_data.get("secret_key", "django-insecure-dev-key") if vault_data else "django-insecure-dev-key"

# =========================
# DATABASE (POSTGRES)
# =========================
if is_ci():
    # CI usa Postgres del servicio de GitHub Actions
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "sentinels_db",
            "USER": "test",
            "PASSWORD": "test",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }
elif vault_data and "database" in vault_data:
    # Local / Prod → Usa datos de Vault
    db = vault_data["database"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db["name"],
            "USER": db["user"],
            "PASSWORD": db["password"],
            "HOST": db["host"],   # postgres
            "PORT": db["port"],   # 5432
        }
    }
else:
    # Fallback: Local con Docker Compose (si Vault falla o no tiene datos)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'sentinels_db',
            'USER': 'admin',       
            'PASSWORD': 'superadmin',
            'HOST': 'postgres',     
            'PORT': '5432',
        }
    }

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "core",
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"