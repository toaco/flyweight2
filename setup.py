from io import open
from os import path

from setuptools import setup, find_packages

import flyweight2

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flyweight2',

    version=flyweight2.__version__,

    description='A variant of the Flyweight pattern that allows the object to be modified without affecting other objects, and automatically shares the memory if the modified object is the same as other objects',
    long_description=long_description,

    url='https://github.com/jefffffrey/flyweight2',

    author='Jeffrey',
    author_email='Jeffrey.S.Teo@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    platforms='any',

    keywords=['flyweight', 'flyweight-pattern', 'objectpool', 'shared-memory'],

    packages=find_packages(exclude=['test*']),

    install_requires=[],

    extras_require={
        'dev': ['pytest', 'pytest-cov'],
    },

    python_requires='==2.7.*',
)
