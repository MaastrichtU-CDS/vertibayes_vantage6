from os import path
from codecs import open
from setuptools import setup, find_packages

# get current directory
here = path.abspath(path.dirname(__file__))

# get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# # read the API version from disk
# with open(path.join(here, 'vantage6', 'tools', 'VERSION')) as fp:
#     __version__ = fp.read()

# setup the package
setup(
    name='v6_test_py',
    version="1.0.0",
    description='vantage6 test algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/fvandaalen/verticaldt',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'vantage6',
        'pandas'
    ]
)
