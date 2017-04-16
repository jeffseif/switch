from setuptools import setup

from switch import __author__
from switch import __email__
from switch import __program__
from switch import __url__
from switch import __version__


setup(
    author=__author__,
    author_email=__email__,
    dependency_links=[
        'https://github.com/jeffseif/colors.git#egg=colors',
    ],
    install_requires=[
        'beautifulsoup4>=4.5.3',
        'requests>=2.9.1',
    ],
    name=__program__,
    packages=[__program__],
    platforms='all',
    setup_requires=[
        'setuptools',
        'tox',
    ],
    test_suite='tests',
    url=__url__,
    version=__version__,
)
