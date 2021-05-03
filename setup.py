from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = ''.join(f.readlines())

setup(
    name='pypgqueue',
    version='0.1.0',
    keywords='postgres queue messaging testing',
    description='Testing of producer/consumer queue with PostgreSQL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Marek Suchánek',
    url='https://github.com/ds-wizard/dsw-tdk',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pypgqueue = pypgqueue:main',
        ]
    },
    install_requires=[
        'click',
        'colorama',
        'psycopg2',
    ],
    python_requires='>=3.8, <4',
    zip_safe=False,
)
