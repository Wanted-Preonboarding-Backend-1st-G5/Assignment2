from .base   import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
DEBUG      = True

NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEOMODEL_NEO4J_BOLT_URL', 'bolt://neo4j:test@localhost:7687')
NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_MAX_CONNECTION_POOL_SIZE = 50