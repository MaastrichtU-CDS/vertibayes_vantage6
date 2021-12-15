import subprocess
import os

DEFAULT_PORT = 8888


def RPC_init(client):
    # TODO: Create properties file
    subprocess.run(f'java -jar {_get_jar_path()}')


def _get_jar_path():
    return os.environ.get('JAR_PATH')
