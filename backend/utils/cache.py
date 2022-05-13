import bmemcached
from settings import config

mc = bmemcached.Client(
    config.MEMCACHIER_SERVERS,
    username=config.MEMCACHIER_USERNAME,
    password=config.MEMCACHIER_PASSWORD
)