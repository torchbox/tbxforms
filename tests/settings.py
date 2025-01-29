"""
MVS (Minimalist Viable Settings) for running the tests.
"""

INSTALLED_APPS = (
    "crispy_forms",
    "tbxforms",
)

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ("tbxforms",)

CRISPY_TEMPLATE_PACK = "tbxforms"

CRISPY_FAIL_SILENTLY = False
