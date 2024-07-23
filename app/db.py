import pathlib
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from . import config

settings = config.get_settings()

BASE_DIR = pathlib.Path(__file__).resolve().parent

CONNECT_BUNDLE = BASE_DIR / 'unencrypted' / 'secure-connect-video-management-project.zip'
with open(BASE_DIR / 'unencrypted' / 'token.json') as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

def get_session():
    cloud_config= {
        'secure_connect_bundle': str(CONNECT_BUNDLE)
    }
    auth_provider = PlainTextAuthProvider(username=str(CLIENT_ID), password=str(CLIENT_SECRET))
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    # register connection (for FastAPI)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    return session