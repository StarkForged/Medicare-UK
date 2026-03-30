"""
Medicare UK — Django Settings

All sensitive values (SECRET_KEY, DATABASE_URL, etc.) are read from
a .env file using python-decouple. Copy .env.example to .env to get started.
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Security
# ------------------------------------------------------------------
SECRET_KEY   = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG        = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# ------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',

    # Our apps
    'accounts.apps.AccountsConfig',
    'core.apps.CoreConfig',
    'shifts.apps.ShiftsConfig',
    'workers.apps.WorkersConfig',
    'compliance.apps.ComplianceConfig',
    'trust.apps.TrustConfig',
    'admin_panel.apps.AdminPanelConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    # serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medicare_uk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # project-level templates folder (optional)
        'APP_DIRS': True,                   # Django also looks in each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Our custom processor — injects notification counts into every template
                'core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'medicare_uk.wsgi.application'

# ------------------------------------------------------------------
# Database — SQLite by default, swap to PostgreSQL for production
# ------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Tell Django to use our custom User model instead of the default one
AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL  = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ------------------------------------------------------------------
# Internationalisation
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-gb'
TIME_ZONE     = 'Europe/London'
USE_I18N      = True
USE_TZ        = True

# ------------------------------------------------------------------
# Static & Media files
# ------------------------------------------------------------------
STATIC_URL       = '/static/'
STATIC_ROOT      = BASE_DIR / 'staticfiles'          # where collectstatic writes to
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']    # extra folders Django scans
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------
# Misc
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'
