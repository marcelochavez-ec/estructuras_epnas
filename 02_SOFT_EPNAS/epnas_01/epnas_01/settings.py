import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# EPNAS 01 - CONFIGURACIÓN DJANGO
# Base PostgreSQL: productos_bm
# Schema: epnas
# ============================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "epnas-01-dev-change-this-key-before-production")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

DB_SCHEMA = "epnas"

INSTALLED_APPS = [
    "unfold",  # Debe ir antes de django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "epnas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "epnas_01.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "epnas_01.wsgi.application"
ASGI_APPLICATION = "epnas_01.asgi.application"

# ============================================================
# POSTGRESQL
# Las credenciales se leen desde variables de entorno para evitar publicar
# secretos institucionales en el repositorio.
# ============================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("EPNAS_DB_NAME", "productos_bm"),
        "USER": os.getenv("EPNAS_DB_USER", ""),
        "PASSWORD": os.getenv("EPNAS_DB_PASSWORD", ""),
        "HOST": os.getenv("EPNAS_DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("EPNAS_DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "options": f"-c search_path={DB_SCHEMA},public",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "epnas:inicio"
LOGOUT_REDIRECT_URL = "login"

UNFOLD = {
    "SITE_TITLE": "EPNAS",
    "SITE_HEADER": "EPNAS | Ministerio de Salud Pública",
    "SITE_SUBHEADER": "Sistema de Formulario Web",
    "SITE_SYMBOL": "health_and_safety",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
}
