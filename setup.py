import os
import setuptools

from setuptools import setup


setup(
    name='pg_events',
    version='0.1.2b0',
    description="Postgres events",
    long_description='',
    keywords='postgres python trigger listen notify events',
    author='ZeroCater',
    author_email='tech@zerocater.com',
    url='https://github.com/ZeroCater/pg_events',
    download_url='https://github.com/ZeroCater/pg_events/tarball/0.1.2b0',
    license='MIT',
    packages=setuptools.find_packages(),
    package_data={'pg_events': ['core/schemas/*.sql']},
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
