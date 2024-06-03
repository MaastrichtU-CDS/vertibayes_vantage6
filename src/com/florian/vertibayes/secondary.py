import os
import subprocess

from vantage6.algorithm.tools.decorators import data
from vantage6.algorithm.tools.util import get_env_var

from vantage6.common import info

DEFAULT_PORT = 8888
DATABASE_URI = "DATABASE_URI"


@data(1)
def init(*args, **kwargs):
    info('Starting java server')


    label = get_env_var("USER_REQUESTED_DATABASE_LABELS").split(",")[0]
    # This is how vantage6 passes database uri to the algorithm
    target_uri = get_env_var(f"{label.upper()}_DATABASE_URI")

    env = os.environ
    env["DATABASE_URI"] = target_uri

    # TODO: Create properties file
    subprocess.run(['java', '-jar', _get_jar_path()])


def _get_jar_path():
    return os.environ.get('JAR_PATH')


def init_local():
    process = subprocess.Popen(['java', '-jar', _get_jar_path()])
    return process
