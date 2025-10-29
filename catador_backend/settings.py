# catador_backend/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Carga .env en local; en Render usa env vars del panel

# ===== Seguridad / Entorno =====
SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-key-CHANGE-ME"
DEBUG = os.getenv("DEBUG", "1") == "1"

# Hosts permitidos (local + Render)
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
_default_hosts = ["127.0.0.1", "localhost", "192.168.18.25", "192.168.18.24"]
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", ",".join(_default_hosts)).split(",") if h.strip()]
if RENDER_HOST and RENDER_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_HOST)

# ===== Apps =====
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # terceros
    "rest_framework",
    "corsheaders",
    # local
    "inference",
]

# ===== Middleware =====
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # servir estáticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "inference.middleware.APILoggingMiddleware",
]

ROOT_URLCONF = "catador_backend.urls"

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

WSGI_APPLICATION = "catador_backend.wsgi.application"

# ===== Base de datos =====
# Por defecto, SQLite. Si hay DATABASE_URL (Render Postgres), úsala.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ===== Internacionalización =====
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

# ===== Archivos estáticos (WhiteNoise) =====
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== CORS / CSRF =====
# En dev permite todo; en prod define FRONTEND_ORIGINS (coma-separado)
CORS_ALLOW_ALL_ORIGINS = DEBUG
_front = os.getenv("FRONTEND_ORIGINS", "")
if _front and not DEBUG:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _front.split(",") if o.strip()]

CSRF_TRUSTED_ORIGINS = []
if RENDER_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOST}")
_extra_csrf = os.getenv("CSRF_TRUSTED_EXTRA", "")
if _extra_csrf:
    CSRF_TRUSTED_ORIGINS += [u.strip() for u in _extra_csrf.split(",") if u.strip()]

# Proxy SSL (Render) + cookies seguras en prod
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# ===== Modelo ML =====
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "modelo_eval_senso_xgb.pkl"))

# ===== Logging =====
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{levelname}] {asctime} {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "django.server": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "api": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
