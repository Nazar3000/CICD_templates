from service.settings import *  # noqa

TEST_MODE = True

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
LPA_PASSWORD = ""

MIDDLEWARE = [i for i in MIDDLEWARE if i != "service.middlewares.moesif_middlewares.CustomMoesifMiddleware"]  # noqa  # noqa
