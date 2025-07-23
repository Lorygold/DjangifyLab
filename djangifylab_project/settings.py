import os

import environ
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = config("DJANGO_SECRET_KEY", default="fallback-secret")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # TODO: Custom installed app (add manually here after installing the .tar.gz)
    "impossible_travel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

ROOT_URLCONF = "djangifylab_project.urls"
WSGI_APPLICATION = "djangifylab_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env("DB_NAME", default=os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": env("DB_USER", default=""),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default=""),
        "PORT": env("DB_PORT", default=""),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TODO: ADD env variables used in your app
OPTIONAL_ENV_VARS = [
    "CERTEGO_BUFFALOGS_CONFIG_PATH",
    "CERTEGO_BUFFALOGS_IGNORED_USERS",
    "CERTEGO_BUFFALOGS_ENABLED_USERS",
    "CERTEGO_BUFFALOGS_ALLOWED_COUNTRIES",
    "CERTEGO_BUFFALOGS_IGNORED_IPS",
    "CERTEGO_BUFFALOGS_IGNORED_ISPS",
    "CERTEGO_BUFFALOGS_VIP_USERS",
    "CERTEGO_BUFFALOGS_RISK_SCORE_INCREMENT_ALERTS",
    "CERTEGO_BUFFALOGS_DISTANCE_KM_ACCEPTED",
    "CERTEGO_BUFFALOGS_VEL_TRAVEL_ACCEPTED",
    "CERTEGO_BUFFALOGS_ATYPICAL_COUNTRY_DAYS",
    "CERTEGO_BUFFALOGS_USER_MAX_DAYS",
    "CERTEGO_BUFFALOGS_LOGIN_MAX_DAYS",
    "CERTEGO_BUFFALOGS_ALERT_MAX_DAYS",
    "CERTEGO_BUFFALOGS_IP_MAX_DAYS",
    "CERTEGO_BUFFALOGS_MOBILE_DEVICES",
]

# Auto-import custom variables from `.env`
for var in OPTIONAL_ENV_VARS:
    try:
        globals()[var] = config(var)
    except Exception:
        print(f"Optional variable '{var}' not found in .env")
