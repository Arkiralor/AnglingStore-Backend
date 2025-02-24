DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_cron',
    'django_rq',
]

CUSTOM_APPS = [
    'admin_app.apps.AdminAppConfig',
    'communications_app.apps.CommunicationsAppConfig',
    'inventory_app.apps.InventoryAppConfig',
    'job_handler_app.apps.JobHandlerAppConfig',
    'middleware_app.apps.MiddlewareAppConfig',
    'store_app.apps.StoreAppConfig',
    'user_app.apps.UserAppConfig'
]