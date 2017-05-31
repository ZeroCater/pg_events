import os

from setuptools import setup


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='pg_events',
    version='0.0.4',
    description="Postgres events",
    long_description='',
    keywords='postgres python trigger listen notify events',
    author='ZeroCater',
    author_email='tech@zerocater.com',
    url='https://github.com/ZeroCater/pg_events',
    download_url='https://github.com/ZeroCater/pg_events/tarball/0.0.4',
    license='MIT',
    packages=get_packages('pg_events'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        'psycopg2>=2.6,<2.8'
    ],
    entry_points={
        'console_scripts': [
            'pg_events = pg_events.__main__:main',
        ],
    },
)
