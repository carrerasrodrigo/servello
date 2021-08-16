import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='servello',
    version='0.0.0',
    packages=['app'],
    include_package_data=True,
    license='BSD License',
    description='',
    long_description=README,
    url='',
    author='Rodrigo N. Carreras',
    author_email='carrerasrodrigo@gmail.com',
    install_requires=['click', 'flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'servello = app.server:start_app'
        ]
    }
)
