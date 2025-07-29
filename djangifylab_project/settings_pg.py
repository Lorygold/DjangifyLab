import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "djangifylab",
        "USER": "django",
        "PASSWORD": "django",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# TODO: ADD env variables used in your app
CERTEGO_BUFFALOGS_CONFIG_PATH = os.getenv("CERTEGO_BUFFALOGS_CONFIG_PATH", "app_config_files")
CERTEGO_BUFFALOGS_IGNORED_USERS = os.getenv("CERTEGO_BUFFALOGS_IGNORED_USERS", ["Not Available", "N/A"])
CERTEGO_BUFFALOGS_ENABLED_USERS = os.getenv("CERTEGO_BUFFALOGS_ENABLED_USERS", [])
CERTEGO_BUFFALOGS_ALLOWED_COUNTRIES = os.getenv("CERTEGO_BUFFALOGS_ALLOWED_COUNTRIES", [])
CERTEGO_BUFFALOGS_IGNORED_IPS = os.getenv("CERTEGO_BUFFALOGS_IGNORED_IPS", ["127.0.0.1"])
CERTEGO_BUFFALOGS_IGNORED_ISPS = os.getenv("CERTEGO_BUFFALOGS_IGNORED_ISPS", [])
CERTEGO_BUFFALOGS_VIP_USERS = os.getenv("CERTEGO_BUFFALOGS_VIP_USERS", [])
CERTEGO_BUFFALOGS_DISTANCE_KM_ACCEPTED = os.getenv("CERTEGO_BUFFALOGS_DISTANCE_KM_ACCEPTED", 100)
CERTEGO_BUFFALOGS_VEL_TRAVEL_ACCEPTED = os.getenv("CERTEGO_BUFFALOGS_VEL_TRAVEL_ACCEPTED", 300)
CERTEGO_BUFFALOGS_USER_MAX_DAYS = os.getenv("CERTEGO_BUFFALOGS_USER_MAX_DAYS", 60)
CERTEGO_BUFFALOGS_LOGIN_MAX_DAYS = os.getenv("CERTEGO_BUFFALOGS_LOGIN_MAX_DAYS", 45)
CERTEGO_BUFFALOGS_ALERT_MAX_DAYS = os.getenv("CERTEGO_BUFFALOGS_ALERT_MAX_DAYS", 45)
CERTEGO_BUFFALOGS_IP_MAX_DAYS = os.getenv("CERTEGO_BUFFALOGS_IP_MAX_DAYS", 45)
CERTEGO_BUFFALOGS_ATYPICAL_COUNTRY_DAYS = os.getenv("CERTEGO_BUFFALOGS_ATYPICAL_COUNTRY_DAYS", 30)
CERTEGO_BUFFALOGS_MOBILE_DEVICES = os.getenv("CERTEGO_BUFFALOGS_MOBILE_DEVICES", ["iOS", "Android", "Windows Phone"])
CERTEGO_BUFFALOGS_RISK_SCORE_INCREMENT_ALERTS = os.getenv("CERTEGO_BUFFALOGS_RISK_SCORE_INCREMENT_ALERTS", ["New Country", "Anonymous IP Login", "Atypical Country", "Imp Travel"])
