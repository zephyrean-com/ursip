from django.conf import settings


def get_sqlalchemy_engine_url():
    name = settings.DATABASES['default']['NAME']
    return f'sqlite:///{name}'
